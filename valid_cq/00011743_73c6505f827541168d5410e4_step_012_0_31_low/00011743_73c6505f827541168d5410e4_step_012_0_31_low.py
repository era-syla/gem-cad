import cadquery as cq

# Parameters
length = 100.0
width = 40.0
thickness = 5.0
corner_radius = 5.0
hole_dia = 5.0
hole_spacing_x = 20.0
hole_spacing_y = 20.0
num_holes_x = 5
num_holes_y = 2

# Create the base plate with rounded corners
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Add the grid of holes
pts = [
    (x * hole_spacing_x - (num_holes_x - 1) * hole_spacing_x / 2, 
     y * hole_spacing_y - (num_holes_y - 1) * hole_spacing_y / 2)
    for x in range(num_holes_x)
    for y in range(num_holes_y)
]

result = result.faces(">Z").workplane().pushPoints(pts).hole(hole_dia)