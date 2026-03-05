import cadquery as cq

# Parametric dimensions for the rectangular prism
length = 100.0
width = 20.0
height = 20.0

# Create the rectangular bar geometry
# The box method creates a cube/prism centered at the origin
result = cq.Workplane("XY").box(length, width, height)