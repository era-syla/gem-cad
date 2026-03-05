import cadquery as cq

# Define parametric dimensions based on the visual proportions of the image
length = 100.0
width = 25.0
height = 10.0

# Create the rectangular box geometry
# We create a workplane on the XY plane and generate a box
# centered at the origin with the specified dimensions.
result = cq.Workplane("XY").box(length, width, height)