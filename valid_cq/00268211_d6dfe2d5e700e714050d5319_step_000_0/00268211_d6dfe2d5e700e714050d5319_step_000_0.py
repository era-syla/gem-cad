import cadquery as cq

# Parameters definition
length = 80.0
width = 40.0
height = 20.0
fillet_radius = 8.0

# Create the 3D model
# 1. Create a base rectangular box
# 2. Select the top face (Z direction)
# 3. Select the edges parallel to the X-axis on that face
# 4. Apply a fillet to round the edges
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Z")
    .edges("|X")
    .fillet(fillet_radius)
)