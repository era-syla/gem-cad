import cadquery as cq

# Parameters
length = 100.0
width = 20.0
thickness = 10.0

# Create the 3D model
result = cq.Workplane("XY").box(length, width, thickness)