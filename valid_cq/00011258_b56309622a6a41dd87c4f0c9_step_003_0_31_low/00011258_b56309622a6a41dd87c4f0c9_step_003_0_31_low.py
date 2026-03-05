import cadquery as cq

# Parameters
width = 100.0
length = 150.0
thickness = 2.0

# Create the model
result = cq.Workplane("XY").box(width, length, thickness)