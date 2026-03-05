import cadquery as cq

# Define parametric dimensions for the beam
length = 300.0
width = 10.0
height = 10.0

# Create a solid rectangular prism (box) centered at the origin
result = cq.Workplane("XY").box(length, width, height)