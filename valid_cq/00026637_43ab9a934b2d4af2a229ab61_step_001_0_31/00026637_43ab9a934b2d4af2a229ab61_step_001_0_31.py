import cadquery as cq

# Parametric dimensions
length = 100.0
width = 20.0
height = 80.0

# Create the rectangular cuboid
result = cq.Workplane("XY").box(length, width, height)