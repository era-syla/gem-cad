import cadquery as cq

# Define parametric dimensions for the cube
length = 10.0
width = 10.0
height = 10.0

# Create the solid cube geometry
# box() creates a cube centered at the origin by default, 
# or corner-aligned if specified. Here we center it.
result = cq.Workplane("XY").box(length, width, height)

# Alternatively, if you prefer corner alignment:
# result = cq.Workplane("XY").box(length, width, height, centered=False)