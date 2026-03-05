import cadquery as cq

# Define parameters for the cube dimensions
# Since the image shows a perfect cube with equal sides
length = 10.0
width = 10.0
height = 10.0

# Create a simple box (cube) centered at the origin
# The Box operation creates a solid block with the specified dimensions
result = cq.Workplane("XY").box(length, width, height)

# The 'result' variable now contains the CadQuery object representing the cube