import cadquery as cq

# Parametric dimensions for the long rectangular bar
length = 300.0
width = 4.0
height = 4.0

# Create the geometry
# Generates a solid box centered at the origin
result = cq.Workplane("XY").box(length, width, height)