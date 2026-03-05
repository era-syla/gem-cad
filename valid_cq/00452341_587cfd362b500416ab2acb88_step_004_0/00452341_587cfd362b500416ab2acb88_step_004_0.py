import cadquery as cq

# Parametric dimensions for the rectangular prism
length = 100.0
width = 30.0
height = 30.0

# Create the box geometry
# We use the XY plane and center the box at the origin
result = cq.Workplane("XY").box(length, width, height)