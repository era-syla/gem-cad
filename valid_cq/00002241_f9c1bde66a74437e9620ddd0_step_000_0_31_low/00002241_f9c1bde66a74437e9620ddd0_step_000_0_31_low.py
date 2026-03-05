import cadquery as cq

# Parameters
length = 100.0
width = 30.0
thickness = 20.0
point_length = 20.0
pocket_length = 60.0
pocket_width = 15.0
pocket_depth = 5.0

# Create the main body
pts = [
    (length / 2 - point_length, width / 2),
    (length / 2, 0),
    (length / 2 - point_length, -width / 2),
    (-(length / 2 - point_length), -width / 2),
    (-length / 2, 0),
    (-(length / 2 - point_length), width / 2),
]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .rect(pocket_length, pocket_width)
    .cutBlind(-pocket_depth)
)