import cadquery as cq

# Dimensions
width = 120.0
height = 70.0
thickness = 8.0
fillet_radius = 3.0

# Hole dimensions
hole_dia = 6.0
csk_dia = 12.0
csk_angle = 90.0

# Hole positioning
margin_x = 15.0
margin_y = 15.0
dx = (width / 2) - margin_x
dy = (height / 2) - margin_y

# Points for the holes: 3 on top row, 2 on bottom row
hole_points = [
    (-dx, dy), (0, dy), (dx, dy),   # Top Row: Left, Middle, Right
    (-dx, -dy),         (dx, -dy)   # Bottom Row: Left, Right
]

# Create the model
result = (
    cq.Workplane("XY")
    .box(width, height, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_points)
    .cskHole(hole_dia, csk_dia, csk_angle)
)