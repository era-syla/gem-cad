import cadquery as cq

# --- Parameters ---
# Overall Dimensions
total_height = 80.0
base_radius_outer = 40.0
base_radius_inner = 30.0
base_thickness = 10.0

# X-Structure (Hourglass) Dimensions
x_struct_thickness = 10.0
x_struct_width_top = 60.0
x_struct_width_bottom = 60.0
waist_width = 15.0  # Narrowest part of the X

# Top Bar Dimensions
top_bar_length = 100.0
top_bar_width = 15.0
top_bar_height = 10.0

# Small Post Dimensions
post_side = 12.0
post_height = 30.0

# --- Geometry Construction ---

# 1. Base: Semi-circular ring
# Create a full ring first, then cut it to make it a semi-circle
base = (
    cq.Workplane("XY")
    .circle(base_radius_outer)
    .circle(base_radius_inner)
    .extrude(base_thickness)
)

# Cut the base to make it a semi-circle (keeping the back half roughly where the structure will be)
# We create a large box to subtract the front half
cut_box = (
    cq.Workplane("XY")
    .rect(base_radius_outer * 2.5, base_radius_outer * 2.5)
    .extrude(base_thickness)
    .translate((0, -base_radius_outer * 1.25, 0)) # Shift to cut the negative Y half
)

base_semi = base.cut(cut_box)


# 2. X-Structure (Hourglass shape)
# We will draw this on the XZ plane (front view) and extrude along Y
# Points for the X shape
x_half_top = x_struct_width_top / 2.0
x_half_bot = x_struct_width_bottom / 2.0
waist_half = waist_width / 2.0
height_start = base_thickness
height_end = total_height - top_bar_height
mid_height = (height_start + height_end) / 2.0

# Define points for a polygon forming the X shape
pts = [
    (-x_half_bot, height_start),   # Bottom Left
    (x_half_bot, height_start),    # Bottom Right
    (waist_half, mid_height),      # Middle Right (waist)
    (x_half_top, height_end),      # Top Right
    (-x_half_top, height_end),     # Top Left
    (-waist_half, mid_height),     # Middle Left (waist)
]

x_structure = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .extrude(x_struct_thickness)
    # Center the extrusion on the Y axis
    .translate((0, -x_struct_thickness / 2.0, 0))
)

# 3. Top Bar
top_bar = (
    cq.Workplane("XY")
    .rect(top_bar_length, top_bar_width)
    .extrude(top_bar_height)
    .translate((0, 0, total_height - top_bar_height))
)

# 4. Small Post
# Positioned on one side of the semi-circle
post_x_pos = -(base_radius_inner + (base_radius_outer - base_radius_inner)/2)
post = (
    cq.Workplane("XY")
    .rect(post_side, post_side)
    .extrude(post_height)
    .translate((post_x_pos, 0, 0)) # Position on the left arm of the semi-circle
)

# --- Combine All Parts ---

result = base_semi.union(x_structure).union(top_bar).union(post)
