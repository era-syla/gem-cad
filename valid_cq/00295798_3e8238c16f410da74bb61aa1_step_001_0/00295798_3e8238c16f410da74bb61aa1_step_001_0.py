import cadquery as cq

# Parametric dimensions
block_length = 100.0
block_width = 30.0
block_height = 30.0

slot_length = 50.0
slot_width = 8.0
slot_depth = 10.0
slot_offset_from_edge = 10.0  # Distance from the end of the block to the start of the slot

# Calculate the center position of the slot relative to the block's coordinate system
# Assuming block is centered at origin, left edge is at x = -block_length/2
x_left_edge = -block_length / 2.0
slot_center_x = x_left_edge + slot_offset_from_edge + (slot_length / 2.0)

# Create the model
result = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_height)
    .faces(">Z")
    .workplane()
    .center(slot_center_x, 0)
    .slot2D(slot_length, slot_width)
    .cutBlind(-slot_depth)
)