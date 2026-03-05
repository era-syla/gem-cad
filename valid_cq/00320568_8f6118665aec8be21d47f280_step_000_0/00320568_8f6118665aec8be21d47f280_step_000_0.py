import cadquery as cq

# Define parametric dimensions based on the visual proportions of the image
length = 100.0
width = 50.0
height = 15.0

# Create the rectangular prism (box) geometry
# box() creates a cube centered at the origin by default
result = cq.Workplane("XY").box(length, width, height)