import cadquery as cq

# Parametric dimensions
length = 100.0
width = 70.0
thickness = 5.0

# Create the rectangular plate
result = cq.Workplane("XY").box(length, width, thickness)