import cadquery as cq

# Define parametric dimensions
length = 100.0
width = 20.0
height = 20.0

# Create a rectangular prism (box) centered at the origin
result = cq.Workplane("XY").box(length, width, height)