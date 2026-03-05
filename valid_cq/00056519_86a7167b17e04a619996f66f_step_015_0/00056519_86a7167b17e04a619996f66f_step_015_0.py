import cadquery as cq

# Define parametric dimensions based on visual proportions
length = 100.0
width = 40.0
height = 10.0

# Create a simple rectangular prism (box)
# The box is centered on the XY plane
result = cq.Workplane("XY").box(length, width, height)