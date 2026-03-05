import cadquery as cq

# Parametric dimensions
# Main long block dimensions
long_block_length = 40.0
long_block_width = 20.0
long_block_height = 8.0

# Cube/End block dimensions
cube_size = 20.0  # Making it a cube for simplicity, height matches the width of the long block

# Create the long rectangular block
# We'll center it on the Y axis to make alignment easier, but extend along X
long_block = cq.Workplane("XY").box(long_block_length, long_block_width, long_block_height, centered=(False, True, False))

# Create the larger cube block at the end
# We need to position it at the end of the long block
# The long block starts at x=0 and ends at x=long_block_length
cube_block = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start at z=0 base
    .moveTo(long_block_length, 0) # Move to the end of the first block
    .box(cube_size, cube_size, cube_size, centered=(False, True, False))
)

# Combine the two parts into a single object
result = long_block.union(cube_block)

# If running in an environment that supports show_object (like CQ-Editor), this will display it
# show_object(result)