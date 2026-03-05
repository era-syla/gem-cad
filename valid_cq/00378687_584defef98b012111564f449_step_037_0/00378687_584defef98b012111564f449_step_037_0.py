import cadquery as cq

# Parametric dimensions for the plate
length = 100.0
width = 80.0
thickness = 5.0

# Create a rectangular plate (box) centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)