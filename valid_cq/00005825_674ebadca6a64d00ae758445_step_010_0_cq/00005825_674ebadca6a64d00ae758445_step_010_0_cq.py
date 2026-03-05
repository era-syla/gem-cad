import cadquery as cq

# Parametric dimensions
length = 50.0  # Length of the box (x-axis)
width = 50.0   # Width of the box (y-axis)
height = 50.0  # Height of the box (z-axis)
thickness = 2.0 # Wall thickness

# Create the main box
# We start with a solid block and then shell it to create the hollow shape with an open top.
# Using centered=False puts one corner at the origin, usually easier for inspection. 
# Using centered=(True, True, False) centers it on X and Y, sitting on the Z plane.
result = (
    cq.Workplane("XY")
    .box(length, width, height, centered=(True, True, False))
    .faces("+Z") # Select the top face
    .shell(-thickness) # Shell inwards by the thickness amount to create walls and floor
)