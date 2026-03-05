import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the box
width = 50.0    # Width of the box
height = 25.0   # Height of the box

# Create a rectangular block (box) centered at the origin
# The box method creates a box with the specified dimensions.
# By default, it creates the box centered on the current workplane (XY plane).
result = cq.Workplane("XY").box(length, width, height)

# Alternatively, if you want it sitting on the XY plane (not centered in Z):
# result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))