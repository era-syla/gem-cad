import cadquery as cq

# --- Parameters ---
# Base plate dimensions
plate_thickness = 2.0
wing_points = [(0, 0), (80, -40), (110, -10), (100, 40), (20, 20)]
hole_diam_plate = 3.0
# Approximate hole positions on the right wing
plate_holes = [(70, -20), (95, -5), (50, 20)]

# Rod dimensions
rod_diam = 6.0
rod_length = 300.0
rod_offset_z = -10.0  # Rod extends slightly below the plate
rod_pos_xy = (40, 20)  # Position of the rod on the right wing

# Top block dimensions
block_w = 16.0
block_d = 10.0
block_h = 14.0
block_hole_diam = 3.0
block_hole_spacing = 6.0

# --- Geometry Construction ---

# 1. Create the Right Wing
# Draw polygon, extrude, and cut holes
right_wing = (
    cq.Workplane("XY")
    .polyline(wing_points)
    .close()
    .extrude(plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(plate_holes)
    .hole(hole_diam_plate)
)

# 2. Create the Left Wing (Mirror of Right Wing)
left_wing = right_wing.mirror(mirrorPlane="YZ")

# Combine wings into base assembly
base = right_wing.union(left_wing)

# 3. Create the Vertical Rod
# Create a cylinder at the specified position
rod = (
    cq.Workplane("XY")
    .workplane(offset=rod_offset_z)
    .center(*rod_pos_xy)
    .circle(rod_diam / 2.0)
    .extrude(rod_length + abs(rod_offset_z))
)

# 4. Create the Top Sensor Block
# Box on top of the rod
top_block_z = rod_length + rod_offset_z - 5 # Adjust so rod goes slightly into or flush with block
# Let's place it exactly at the top of the declared rod length relative to Z=0
block_center_z = rod_length - (block_h / 2.0)

# Create the block centered on the rod axis
block = (
    cq.Workplane("XY")
    .workplane(offset=rod_length) # Position at top of rod
    .center(*rod_pos_xy)
    .box(block_w, block_d, block_h, centered=(True, True, False)) # Centered XY, sits on top Z
)

# Add "eyes" (holes) to the block
# Assuming the block faces -Y direction (towards the "V" opening somewhat)
# We select the face, establish a workplane, and drill holes
block_with_holes = (
    block.faces("<Y") # Select the front face
    .workplane()
    .pushPoints([(-block_hole_spacing/2.0, 0), (block_hole_spacing/2.0, 0)]) # Local coordinates on face
    .hole(block_hole_diam)
)

# --- Final Assembly ---
result = base.union(rod).union(block_with_holes)