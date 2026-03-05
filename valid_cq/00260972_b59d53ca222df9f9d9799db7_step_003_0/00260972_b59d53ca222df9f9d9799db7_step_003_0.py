import cadquery as cq

# --- Parameters ---
total_height = 90.0
block_width = 50.0
block_depth = 20.0
block_height = 15.0

spine_width = 20.0
spine_depth = 15.0
serration_radius = 4.5
num_serrations = 4

slot_width = 20.0
pin_hole_diameter = 8.0

# --- Geometry Construction ---

# 1. Create the Bottom Block (Fork/Clevis)
# Base block centered at (0,0) in XY, sitting on Z=0
bottom_block = (
    cq.Workplane("XY")
    .box(block_width, block_depth, block_height)
    .translate((0, 0, block_height / 2))
)

# Create the slot cutout from the front (Positive Y)
# We position the cutter to remove the front-center portion
slot_cutter = (
    cq.Workplane("XY")
    .box(slot_width, block_depth, block_height)
    .translate((0, block_depth / 2, block_height / 2))
)
bottom_block = bottom_block.cut(slot_cutter)

# Create the pin hole running through the X-axis
bottom_block = (
    bottom_block.faces(">X")
    .workplane()
    .circle(pin_hole_diameter / 2)
    .cutThruAll()
)

# 2. Create the Top Block (T-Head)
top_block = (
    cq.Workplane("XY")
    .box(block_width, block_depth, block_height)
    .translate((0, 0, total_height - block_height / 2))
)

# 3. Create the Vertical Spine
# The spine connects the back of the top and bottom blocks.
# We align the back faces. Back face is at Y = -block_depth / 2.
spine_height = total_height - 2 * block_height
spine_center_y = -block_depth / 2 + spine_depth / 2
spine_center_z = block_height + spine_height / 2

spine = (
    cq.Workplane("XY")
    .box(spine_width, spine_depth, spine_height)
    .translate((0, spine_center_y, spine_center_z))
)

# 4. Create Serrations (Scallops) on the Spine
# We cut cylindrical shapes out of the front face of the spine.
spine_front_face_y = -block_depth / 2 + spine_depth

# Calculate vertical distribution of cuts
# Ensure cuts are centered within the spine height with some margin
margin = serration_radius * 1.1
z_start = block_height + margin
z_end = total_height - block_height - margin
z_step = (z_end - z_start) / (num_serrations - 1) if num_serrations > 1 else 0

for i in range(num_serrations):
    z_pos = z_start + i * z_step
    
    # Create a cylindrical cutter oriented along the X-axis
    # Positioned so the circle center is on the front face edge
    cutter = (
        cq.Workplane("YZ")
        .workplane(offset=-block_width)  # Start cutter outside the object
        .center(spine_front_face_y, z_pos)
        .circle(serration_radius)
        .extrude(block_width * 2)  # Cut all the way through
    )
    spine = spine.cut(cutter)

# 5. Combine all parts into the final result
result = bottom_block.union(top_block).union(spine)