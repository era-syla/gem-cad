import cadquery as cq

# Parametric dimensions
length = 100.0
width = 40.0
thickness = 10.0

# Create the rectangular prism (box)
result = cq.Workplane("XY").box(length, width, thickness)