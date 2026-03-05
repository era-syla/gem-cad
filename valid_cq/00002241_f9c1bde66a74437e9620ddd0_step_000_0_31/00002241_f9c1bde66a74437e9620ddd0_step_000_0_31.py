import cadquery as cq

# Parameters for the main body
width = 20.0
straight_length = 40.0
point_length = 10.0
height = 10.0

# Parameters for the top pocket
pocket_length = 26.0
pocket_width = 10.0
pocket_depth = 3.0

# Define the coordinates for the pointed rectangular profile
pts = [
    (straight_length / 2, width / 2),
    (-straight_length / 2, width / 2),
    (-(straight_length / 2 + point_length), 0.0),
    (-straight_length / 2, -width / 2),
    (straight_length / 2, -width / 2),
    ((straight_length / 2 + point_length), 0.0)
]

# Generate the 3D model
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