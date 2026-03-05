import cadquery as cq

# Parametric dimensions
length = 100.0
width = 30.0
thickness = 2.0
corner_radius = 2.0

# Create the rectangular plate with rounded corners
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)