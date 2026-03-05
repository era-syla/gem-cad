import cadquery as cq

# Define parametric dimensions for the rectangular bar
length = 100.0  # Long dimension
width = 20.0    # Width of the profile
height = 20.0   # Height of the profile

# Create a rectangular prism (box) centered at the origin
# The box method takes (length, width, height) arguments
result = cq.Workplane("XY").box(length, width, height)