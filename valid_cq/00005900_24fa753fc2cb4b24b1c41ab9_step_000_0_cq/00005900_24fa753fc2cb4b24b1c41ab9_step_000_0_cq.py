import cadquery as cq

# Parametric dimensions
width = 100.0   # Width of the square plate
length = 100.0  # Length of the square plate
height = 10.0   # Total height/thickness of the plate
chamfer_size = 5.0 # Size of the chamfer on the top edges

# Create the base block
# We create a box centered on X and Y, sitting on the Z plane (or centered on Z)
# Let's align it so the bottom face is on Z=0 for easier mental modeling
result = cq.Workplane("XY").box(width, length, height)

# Select the top face's edges to apply the chamfer
# The selector ">Z" selects the face with the maximum Z coordinate (the top face)
# .edges() gets the edges of that face
result = result.faces(">Z").edges().chamfer(chamfer_size)

# If the requirement is specific about the vertical side height vs chamfer:
# The box creates the total envelope.
# If chamfer_size < height, there will be a vertical section at the bottom.
# Based on the image, the chamfer doesn't go all the way to the bottom, 
# leaving a vertical skirt. This matches the logic above.