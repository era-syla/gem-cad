import cadquery as cq

# Define parametric dimensions based on the visual proportions of the image
length = 100.0
width = 35.0
thickness = 3.0

# Create the rectangular plate geometry
# Using box() creates a solid rectangular prism. 
# By default, it is centered at the origin (0,0,0).
result = cq.Workplane("XY").box(length, width, thickness)