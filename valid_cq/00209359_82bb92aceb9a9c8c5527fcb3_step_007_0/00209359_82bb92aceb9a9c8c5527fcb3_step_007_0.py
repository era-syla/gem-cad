import cadquery as cq

# Parametric dimensions for the plate
length = 100.0
width = 100.0
thickness = 2.0

# Create a rectangular plate (box) centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)