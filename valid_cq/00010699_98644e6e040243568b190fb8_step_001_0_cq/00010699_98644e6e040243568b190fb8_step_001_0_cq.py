import cadquery as cq

# Parametric dimensions for the cube
length = 10.0
width = 10.0
height = 10.0

# Create a simple box (cube) centered at the origin
# The box method creates a box with the specified dimensions centered at the current workplane origin
result = cq.Workplane("XY").box(length, width, height)