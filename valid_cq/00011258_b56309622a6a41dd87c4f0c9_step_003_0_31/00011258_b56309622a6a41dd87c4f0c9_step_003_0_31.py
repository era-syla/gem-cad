import cadquery as cq

# Parametric dimensions
length = 100.0
width = 75.0
thickness = 2.0

# Create the rectangular plate
result = cq.Workplane("XY").box(length, width, thickness)