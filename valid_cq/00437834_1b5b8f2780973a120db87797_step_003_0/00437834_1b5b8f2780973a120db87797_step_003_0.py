import cadquery as cq

# Define parametric dimensions based on the visual aspect ratio
# The image shows an elongated rectangular prism, roughly 3:1:1
length = 60.0
width = 20.0
height = 20.0

# Create the rectangular prism (box)
# Using the XY plane and centering the box at the origin
result = cq.Workplane("XY").box(length, width, height)