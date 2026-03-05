import cadquery as cq

# Parametric dimensions
block_length = 50.0  # X-axis
block_width = 30.0   # Y-axis (thickness)
block_height = 40.0  # Z-axis
groove_radius = 5.0  # Radius of the semicircular groove
slot_width = 10.0    # Width of the rectangular slot cutout
slot_depth = 10.0    # Depth of the rectangular slot cutout

# 1. Create the main block
# Centered on X and Y, sitting on Z=0 for easier visualization
base_block = cq.Workplane("XY").box(block_length, block_width, block_height)

# 2. Create the horizontal semicircular groove
# The groove runs along the X-axis on the front face (min Y face)
# We can cut a cylinder.
# Position: Z center is at block_height/2 roughly? Let's assume mid-height.
# Y position: The center of the cylinder needs to be exactly on the front face to make a perfect half-circle.
# The front face is at y = -block_width/2.
groove = (
    cq.Workplane("YZ")
    .workplane(offset=-block_length/2.0) # Move to the start of the block in X
    .moveTo(-block_width/2.0, 0)         # Move to the edge of the block in Y (which is X in this local plane) and center Z (which is Y in local)
    .circle(groove_radius)
    .extrude(block_length)
)

# 3. Create the rectangular slot/pocket in the middle
# This cuts into the groove deeper into the block.
# It seems to be centered along X.
slot = (
    cq.Workplane("XZ")
    .workplane(offset=-block_width/2.0) # Start from the front face
    .center(0, 0)                       # Center on X and Z axes relative to the block center
    .rect(slot_width, groove_radius * 2) # Width and Height of the slot opening
    .extrude(-slot_depth)               # Cut inwards (negative Y direction)
)

# Combine operations
# We subtract the groove and the slot from the base block.
# Actually, the groove is better done directly on the workplane.

result = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_height)
    # Select the front face (min Y)
    .faces("<Y")
    .workplane()
    # Create the semicircular groove profile
    # Local coordinates: X is global X, Y is global Z
    .moveTo(-block_length/2, 0) # Start far left
    .lineTo(block_length/2, 0)  # Line across
    .lineTo(block_length/2, block_height) # Move away to close shape (dummy path for large cut)
    .lineTo(-block_length/2, block_height)
    .close()
    # Actually, a simpler way is to just cut a cylinder along the edge
)

# Re-evaluating the approach for cleaner code:
# 1. Base Box
# 2. Cut a cylinder along the front edge for the groove.
# 3. Cut a box (pocket) in the center of that groove.

result = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_height)
    
    # Cut the semi-cylindrical groove running along X axis on the front face
    # We position a cylinder at y = -block_width/2, z = 0 (relative to center)
    .cut(
        cq.Workplane("YZ")
        .workplane(offset=-block_length/2) # Start cut from side
        .moveTo(-block_width/2, 0)         # Position center of circle on the face edge
        .circle(groove_radius)
        .extrude(block_length)
    )
    
    # Cut the rectangular pocket in the center
    .cut(
        cq.Workplane("XZ") # Looking from front
        .workplane(offset=-block_width/2) # On the front face
        .rect(slot_width, groove_radius * 2) # Rectangle matching diameter height
        .extrude(-slot_depth) # Extrude inwards (negative Y)
    )
)