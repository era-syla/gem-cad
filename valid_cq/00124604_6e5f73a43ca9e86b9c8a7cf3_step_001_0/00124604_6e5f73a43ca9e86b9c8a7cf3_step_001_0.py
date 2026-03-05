import cadquery as cq

# Define dimensions for the rectangular bar
length = 150.0
width = 12.0
thickness = 3.0

# Create the rectangular prism (box) centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)