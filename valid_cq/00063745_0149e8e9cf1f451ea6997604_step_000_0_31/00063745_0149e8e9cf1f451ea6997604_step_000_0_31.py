import cadquery as cq

# Parametric dimensions
width = 10.0          # Depth of the blocks (Y-axis)
length_left = 10.0    # Length of the left block (X-axis)
length_right = 10.0   # Length of the right block (X-axis)
height = 15.0         # Height of the blocks (Z-axis)
hole_diameter = 2.0   # Diameter of the through-hole

# Create the left rectangular block
left_block = (
    cq.Workplane("XY")
    .center(-length_left / 2.0, 0)
    .box(length_left, width, height)
)

# Create the right rectangular block and drill the hole in its top face center
right_block = (
    cq.Workplane("XY")
    .center(length_right / 2.0, 0)
    .box(length_right, width, height)
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)

# Combine both blocks into the final solid
# (Unioning without .clean() retains the seam shown in the original model)
result = left_block.union(right_block)