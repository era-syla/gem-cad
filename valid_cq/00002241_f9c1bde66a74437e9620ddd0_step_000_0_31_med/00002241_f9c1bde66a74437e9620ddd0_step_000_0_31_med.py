import cadquery as cq

# Parameters for the main body
total_length = 100.0
width = 35.0
height = 20.0
point_length = 20.0

# Parameters for the top pocket
pocket_length = 45.0
pocket_width = 15.0
pocket_depth = 5.0

# Define the 2D profile points for the elongated hexagon
pts = [
    (total_length / 2, 0),
    (total_length / 2 - point_length, width / 2),
    (-total_length / 2 + point_length, width / 2),
    (-total_length / 2, 0),
    (-total_length / 2 + point_length, -width / 2),
    (total_length / 2 - point_length, -width / 2)
]

# Create the base solid and cut the pocket
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height)
    .faces(">Z")
    .workplane()
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)