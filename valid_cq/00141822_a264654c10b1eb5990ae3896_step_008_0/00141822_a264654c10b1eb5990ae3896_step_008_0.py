import cadquery as cq

# Parametric dimensions
length = 60.0
width = 30.0
height = 10.0

# Create the rectangular block
result = cq.Workplane("XY").box(length, width, height)