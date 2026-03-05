import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 100.0
width = 70.0
height = 15.0

# Create the rectangular solid (box)
# using the XY plane as the base
result = cq.Workplane("XY").box(length, width, height)