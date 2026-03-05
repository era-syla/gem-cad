import cadquery as cq

# --- Dimensions ---
# Overall Base Dimensions
base_length = 140.0
base_width = 60.0
base_height = 5.0

# Top Block Dimensions (Stepped in from base)
margin = 2.0
top_length = base_length - (2 * margin)
top_width = base_width - (2 * margin)
top_height = 8.0

# Corner Cutout Details
corner_cutout_radius = 8.5

# Hole Dimensions
# Center Hole (Counterbored)
center_hole_dia = 6.6
center_cb_dia = 11.0
center_cb_depth = 5.0

# Side Mounting Holes (Counterbored)
side_hole_dia = 9.0
side_cb_dia = 14.0
side_cb_depth = 5.0
side_hole_spacing = 38.0  # Distance from center

# Corner Holes (Through the base flange)
corner_hole_dia = 5.5

# End Alignment Holes
end_hole_dia = 2.5
end_hole_depth = 6.0
end_hole_offset_from_edge = 3.5  # Distance from top block edge
end_hole_sep = 12.0  # Separation between the two holes

# --- Modeling ---

# 1. Create the Base Plate
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# 2. Create the Top Block
# We define it separately to handle the corner cutouts cleanly before union
top_block_raw = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .box(top_length, top_width, top_height)
)

# Coordinates for corners of the top block
x_c = top_length / 2.0
y_c = top_width / 2.0
corner_points = [
    (x_c, y_c), (x_c, -y_c),
    (-x_c, y_c), (-x_c, -y_c)
]

# Apply Corner Cutouts to Top Block
# We use hole() which acts as a subtraction
top_block = (
    top_block_raw.faces(">Z")
    .workplane()
    .pushPoints(corner_points)
    .hole(corner_cutout_radius * 2)
)

# 3. Union Base and Top
part = base.union(top_block)

# 4. Add Machining Features (Holes)

# Select top face for drilling
# Note: Drilling from the highest Z face down ensures alignment
part = part.faces(">Z").workplane()

# A. Center Counterbore
part = part.cboreHole(center_hole_dia, center_cb_dia, center_cb_depth)

# B. Side Counterbores
part = (
    part.pushPoints([(side_hole_spacing, 0), (-side_hole_spacing, 0)])
    .cboreHole(side_hole_dia, side_cb_dia, side_cb_depth)
)

# C. Corner Flange Holes
# Locations correspond to the corner cutouts
part = (
    part.pushPoints(corner_points)
    .hole(corner_hole_dia)
)

# D. Small End Alignment Holes
# Calculate positions
x_end = (top_length / 2.0) - end_hole_offset_from_edge
y_end = end_hole_sep / 2.0
end_points = [
    (x_end, y_end), (x_end, -y_end),
    (-x_end, y_end), (-x_end, -y_end)
]

result = (
    part.pushPoints(end_points)
    .hole(end_hole_dia, depth=end_hole_depth)
)