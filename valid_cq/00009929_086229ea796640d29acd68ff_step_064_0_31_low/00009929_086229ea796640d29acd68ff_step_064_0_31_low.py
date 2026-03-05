import cadquery as cq

# Parameters
width = 100.0
length = 100.0
thickness = 5.0

# Create the flat rectangular plate
result = cq.Workplane("XY").box(width, length, thickness)