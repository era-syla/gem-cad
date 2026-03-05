import cadquery as cq

# Geometric Parameters
block_length = 45.0      # Length of the rectangular blocks
block_width = 18.0       # Width of the rectangular blocks
block_height = 4.0       # Thickness/Height of the blocks
center_offset = 12.0     # Distance from the center point to the inner edge of a block

# Calculate the radius for the polar array
# Since polarArray positions the centroid of the sketch, we calculate the distance 
# to the center of the block (offset + half the length)
array_radius = center_offset + (block_length / 2.0)

# Generate the CAD model
# 1. Initialize workplane on XY
# 2. Create a polar array of 4 locations, starting at 45 degrees to match the 'X' orientation
#    rotate=True (default) ensures the local coordinates align radially
# 3. Draw rectangles at each location
# 4. Extrude to create 3D solids
result = (
    cq.Workplane("XY")
    .polarArray(radius=array_radius, startAngle=45, angle=360, count=4)
    .rect(block_length, block_width)
    .extrude(block_height)
)