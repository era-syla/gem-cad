import cadquery as cq

# Parametric dimensions
length = 100.0
width = 50.0
height = 20.0

# Create a simple rectangular prism (box)
# The box is centered at the origin (0,0,0)
result = cq.Workplane("XY").box(length, width, height)