import cadquery as cq

# Main flat bar with rounded ends
length = 80
width = 20
height = 10
hole_diameter = 6
hole_inset = 12

# Create the main body
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(height)
)

# Fillet the vertical edges (long edges on top/bottom faces - the end edges)
result = (
    result
    .edges("|Z")
    .fillet(8)
)

# Add the two mounting holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-length/2 + hole_inset, 0), (length/2 - hole_inset, 0)])
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# Add a small chamfer or step feature on top (the raised center ridge visible in image)
# Looking at the image more carefully, there's a raised tab/ridge in the middle top
# Create a raised center section
ridge_width = 8
ridge_length = length - 30
ridge_height = 3

result = (
    result
    .faces(">Z")
    .workplane()
    .rect(ridge_length, ridge_width)
    .extrude(ridge_height)
)

# Fillet the top edges of the ridge
result = (
    result
    .edges(">Z")
    .fillet(1.5)
)