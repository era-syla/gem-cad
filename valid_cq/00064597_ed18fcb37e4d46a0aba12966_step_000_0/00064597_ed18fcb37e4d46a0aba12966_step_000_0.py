import cadquery as cq

# Define parametric dimensions
length = 80.0
width = 10.0
height = 10.0

# Create the rectangular prism (box)
result = cq.Workplane("XY").box(length, width, height)