import cadquery as cq

# Parametric dimensions
width = 50.0      # Width of one block section
depth = 50.0      # Depth of the blocks
height = 80.0     # Height of the blocks
hole_dia = 12.0   # Diameter of the hole

# Create the left block section
# Positioned to the left of the origin so the seam lies on the YZ plane
left_block = (
    cq.Workplane("XY")
    .center(-width / 2.0, 0)
    .box(width, depth, height)
)

# Create the right block section
# Positioned to the right of the origin
right_block = (
    cq.Workplane("XY")
    .center(width / 2.0, 0)
    .box(width, depth, height)
)

# Add the hole to the right block
# Select the top face (>Z) to create a workplane centered on that face, then cut the hole
right_block_with_hole = (
    right_block
    .faces(">Z")
    .workplane()
    .hole(hole_dia)
)

# Combine the two solids into the final result container
# Note: Using .add() keeps the solids separate within the Workplane, 
# preserving the visual seam line between the two blocks as seen in the image.
result = left_block.add(right_block_with_hole.val())