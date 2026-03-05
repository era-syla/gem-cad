import cadquery as cq

# Parametric dimensions
length = 50.0   # Length of the box base
width = 30.0    # Width of the box base
height = 80.0   # Height of the box
thickness = 3.0 # Wall thickness

# Create the main block
# We start with a solid block centered on X and Y, sitting on the Z=0 plane
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    # Select the top face (positive Z direction)
    .faces(">Z")
    # Shell the solid, removing the selected face to create the hollow interior
    # A negative thickness value shells inwards
    .shell(-thickness)
)