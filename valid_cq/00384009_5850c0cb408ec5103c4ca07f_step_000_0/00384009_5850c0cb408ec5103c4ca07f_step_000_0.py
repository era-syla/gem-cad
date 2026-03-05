import cadquery as cq

# Parametric dimensions
length = 100.0       # Total length of the tube
width = 20.0         # Total width/depth of the tube
height = 50.0        # Total height of the tube
thickness = 2.0      # Wall thickness
radius = 4.0         # External fillet radius of the corners

# Create the model
# 1. Create a solid block representing the outer volume
# 2. Fillet the vertical edges
# 3. Shell the object by removing the top and bottom faces to create a hollow tube
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .edges("|Z")
    .fillet(radius)
    .faces("+Z or -Z")
    .shell(-thickness)
)