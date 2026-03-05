import cadquery as cq

# Parametric dimensions
length = 10.0
width = 10.0
height = 10.0

# Create the solid geometry
# Using cq.Workplane to create a simple box centered at the origin
result = cq.Workplane("XY").box(length, width, height)

# Alternatively, to align with the image's likely orientation (corner facing front):
# The default box is centered. The image is just a view of a cube.
# No special orientation code is strictly needed to generate the geometry itself.