import cadquery as cq

# Parametric dimensions based on the visual aspect ratio
length = 100.0
width = 50.0
height = 30.0

# Create a rectangular cuboid (box)
result = cq.Workplane("XY").box(length, width, height)