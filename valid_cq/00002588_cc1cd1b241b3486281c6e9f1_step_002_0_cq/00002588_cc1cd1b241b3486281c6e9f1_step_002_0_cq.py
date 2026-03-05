import cadquery as cq

# Parametric dimensions
block_length = 50.0  # Length of each block
block_height = 30.0  # Height of each block
block_thickness = 10.0 # Thickness of each block
gap_distance = 40.0 # Distance between the centers of the two blocks

# Create the first block (left side in image)
# We center it on Z to make it "float" if needed, but centering on X/Y is standard practice.
# Let's shift it to one side along the Y axis.
block1 = cq.Workplane("XY").box(block_length, block_thickness, block_height).translate((0, -gap_distance/2, 0))

# Create the second block (right side in image)
# Shift it to the other side along the Y axis.
block2 = cq.Workplane("XY").box(block_length, block_thickness, block_height).translate((0, gap_distance/2, 0))

# Combine the two blocks into a single result
result = block1.union(block2)