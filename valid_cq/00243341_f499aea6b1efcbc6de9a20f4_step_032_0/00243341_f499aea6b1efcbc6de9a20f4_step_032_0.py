import cadquery as cq

# Parametric dimensions
length = 60.0  # Length of the box
width = 20.0   # Width of the box
height = 20.0  # Height of the box

# Create a rectangular prism (box) centered at the origin
result = cq.Workplane("XY").box(length, width, height)