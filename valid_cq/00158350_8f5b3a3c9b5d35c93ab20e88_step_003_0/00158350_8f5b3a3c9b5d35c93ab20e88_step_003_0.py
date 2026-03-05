import cadquery as cq

# Parametric dimensions based on the visual aspect ratio
length = 100.0
width = 5.0
height = 2.5

# Create a rectangular beam/bar
# Using the XY plane and centering the box at the origin
result = cq.Workplane("XY").box(length, width, height)