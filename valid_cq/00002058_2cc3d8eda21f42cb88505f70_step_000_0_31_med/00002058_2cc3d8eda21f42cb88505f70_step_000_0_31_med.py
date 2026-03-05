import cadquery as cq

# Parameters
length = 50.0
width = 10.0
thickness = 5.0

# Create the solid geometry
result = cq.Workplane("XY").box(length, width, thickness)