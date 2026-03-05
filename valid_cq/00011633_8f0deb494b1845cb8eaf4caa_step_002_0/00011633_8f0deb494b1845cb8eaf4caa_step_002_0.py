import cadquery as cq

# --- Dimensions ---
# Main Plate Dimensions
plate_width = 60.0
plate_height = 160.0
plate_thickness = 10.0

# Base Dimensions
base_depth_total = 70.0  # Total depth from back face to front edge
base_fillet_radius = 15.0

# Center Block Dimensions
lower_block_w = 34.0
lower_block_d = 34.0
lower_block_h = 45.0

upper_block_w = 46.0
upper_block_d = 46.0
upper_block_h = 25.0

# Spout Dimensions
spout_dia = 8.0
spout_len = 15.0
spout_angle = 45.0  # Degrees downward

# Hole Dimensions
hole_dia = 5.0
hole_csk_dia = 9.0
hole_csk_angle = 90.0
hole_spacing_x = 30.0
# Z positions for the rows of holes
hole_rows_z = [145, 130, 95, 80] 

# --- Modeling ---

# 1. Back Plate
# Vertical plate on XZ plane, extruded along Y
back_plate = (
    cq.Workplane("XZ")
    .rect(plate_width, plate_height, centered=(True, False))
    .extrude(plate_thickness)
)

# 2. Base Plate
# Horizontal plate on XY plane, extruded along Z
# Starts from the front face of the back plate
base_plate = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(0, plate_thickness) # Align start with front of back plate
    .rect(plate_width, base_depth_total - plate_thickness, centered=(True, False))
    .extrude(plate_thickness)
)

# Apply fillet to the front corners of the base plate
base_plate = base_plate.edges("|Z").edges(">Y").fillet(base_fillet_radius)

# 3. Center Structure
# Lower Block
lower_block = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness) # Sits on base plate
    .center(0, plate_thickness) # Aligns with back plate
    .rect(lower_block_w, lower_block_d, centered=(True, False))
    .extrude(lower_block_h)
)

# Upper Block
upper_block = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness + lower_block_h) # Sits on lower block
    .center(0, plate_thickness)
    .rect(upper_block_w, upper_block_d, centered=(True, False))
    .extrude(upper_block_h)
)

# 4. Angled Spout
# Attached to the front face of the lower block
spout_y_loc = plate_thickness + lower_block_d
spout_z_loc = plate_thickness + (lower_block_h / 2.0)

spout = (
    cq.Workplane("front") # Defines XZ plane with +Y normal
    .workplane(offset=spout_y_loc) # Move to front face of lower block
    .center(0, spout_z_loc)
    .transformed(rotate=(-spout_angle, 0, 0)) # Tilt downwards
    .circle(spout_dia / 2.0)
    .extrude(spout_len)
)

# 5. Union Geometry
result = back_plate.union(base_plate).union(lower_block).union(upper_block).union(spout)

# 6. Create Holes
hole_points = []
for z in hole_rows_z:
    hole_points.append((-hole_spacing_x / 2.0, z))
    hole_points.append((hole_spacing_x / 2.0, z))

# Select the exposed front face of the back plate to drill holes
# We use a point selector high up on the plate to ensure we don't pick the block faces
target_face_selector = cq.NearestToPointSelector((0, plate_thickness, 120))

result = (
    result.faces(target_face_selector)
    .workplane()
    .pushPoints(hole_points)
    .cskHole(hole_dia, hole_csk_dia, hole_csk_angle)
)