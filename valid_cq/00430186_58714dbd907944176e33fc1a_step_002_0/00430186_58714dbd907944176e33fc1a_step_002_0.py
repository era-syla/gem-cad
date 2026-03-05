import cadquery as cq

# Parametric dimensions of the part
length = 100.0        # Total length of the block
width = 50.0          # Total width of the block
height = 20.0         # Total height of the block

# Dimensions of the transverse slot/groove feature
slot_width = 12.0     # Width of the slot (along the length axis)
slot_depth = 5.0      # Depth of the cut from the top face
wall_thickness = 3.0  # Thickness of the lip at the end of the block

# Calculate the position of the slot center relative to the block center
# The block is centered at (0,0,0), so the edge is at length/2.
# We offset inwards by the wall thickness and half the slot width.
slot_center_x = (length / 2) - wall_thickness - (slot_width / 2)

# Generate the model
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Z")
    .workplane()
    .center(slot_center_x, 0)
    .rect(slot_width, width)
    .cutBlind(-slot_depth)
)