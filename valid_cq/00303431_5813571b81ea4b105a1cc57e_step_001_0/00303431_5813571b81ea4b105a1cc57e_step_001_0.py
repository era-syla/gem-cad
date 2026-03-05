import cadquery as cq

# Define parametric dimensions
length = 150.0
width = 12.0
thickness = 3.0

# Create the rectangular bar (rectangular prism)
# The box is centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)