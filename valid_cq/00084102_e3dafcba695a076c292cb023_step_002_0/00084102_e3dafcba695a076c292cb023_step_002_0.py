import cadquery as cq

# Geometric parameters
length = 150.0
width = 25.0
thickness = 2.0

# Create a simple rectangular strip (box)
# The box method creates a rectangular prism centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)