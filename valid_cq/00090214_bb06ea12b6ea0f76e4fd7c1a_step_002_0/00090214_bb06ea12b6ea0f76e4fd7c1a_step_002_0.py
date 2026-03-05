import cadquery as cq

# Parametric dimensions based on visual proportions
length = 100.0
width = 40.0
height = 40.0

# Create a rectangular prism (box)
# The box method centers the object at the origin by default
result = cq.Workplane("XY").box(length, width, height)