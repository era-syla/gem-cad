import cadquery as cq

# Parametric dimensions based on visual estimation of the rectangular plate
length = 100.0
width = 30.0
thickness = 2.0

# Create the simple rectangular plate geometry
result = cq.Workplane("XY").box(length, width, thickness)