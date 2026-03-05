import cadquery as cq

# Define parameters for the cube
length = 10.0
width = 10.0
height = 10.0

# Create the solid cube geometry
# We center it for convenience, but the image is just an isometric view
result = cq.Workplane("XY").box(length, width, height)