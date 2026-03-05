import cadquery as cq

# Parametric dimensions for the model
block_width = 80.0       # Overall width in X
block_depth = 50.0       # Overall depth in Y
block_height = 25.0      # Overall height in Z
slot_width = 30.0        # Width of the cutout
slot_depth = 35.0        # Depth of the cutout
chamfer_size = 15.0      # Size of the corner chamfers

# Generate the geometry
result = (
    cq.Workplane("XY")
    # 1. Create the base rectangular block
    .box(block_width, block_depth, block_height)
    
    # 2. Create the rectangular slot
    # Select the front face (+Y)
    .faces(">Y")
    .workplane()
    # Draw a rectangle for the slot
    # Height is slightly larger than block_height to ensure a clean cut through top/bottom
    .rect(slot_width, block_height + 1.0)
    # Cut inwards (negative direction)
    .cutBlind(-slot_depth)
    
    # 3. Apply chamfers to the back corners
    # Select the back face (-Y)
    .faces("<Y")
    # Select vertical edges on the back face
    .edges("|Z")
    # Chamfer the selected edges
    .chamfer(chamfer_size)
)