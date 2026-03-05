import cadquery as cq

# Define parametric dimensions for the beam
width = 10.0
depth = 10.0
height = 120.0

# Create the rectangular prism (box)
# This creates a solid block centered at the origin
result = cq.Workplane("XY").box(width, depth, height)