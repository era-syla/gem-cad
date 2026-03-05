import cadquery as cq

# Parametric dimensions for the model
# Base plate dimensions
base_length = 100.0
base_width = 70.0
base_thickness = 6.0

# Raised block dimensions
block_length = 40.0
block_width = 25.0
block_height = 4.0

# Positioning: Margin from the edges of the base plate
margin_x = 5.0
margin_y = 5.0

# 1. Create the main base plate
# We start with a box centered on the XY plane
result = cq.Workplane("XY").box(base_length, base_width, base_thickness)

# 2. Add the raised block feature
# Calculate the center position of the block to place it in the corner
# relative to the base plate's dimensions and the specified margins.
# We place it in the +X, +Y quadrant (top-right corner in plan view).
block_center_x = (base_length / 2.0) - margin_x - (block_length / 2.0)
block_center_y = (base_width / 2.0) - margin_y - (block_width / 2.0)

# Select the top face of the base, create a new workplane, shift origin, and add the block
result = (
    result
    .faces(">Z")
    .workplane()
    .center(block_center_x, block_center_y)
    .box(block_length, block_width, block_height, combine=True)
)