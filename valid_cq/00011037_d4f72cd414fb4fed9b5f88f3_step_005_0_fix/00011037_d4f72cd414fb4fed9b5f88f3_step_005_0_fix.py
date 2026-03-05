import cadquery as cq

# Parameters
length = 60
depth = 20
h_small = 10
h_big = 30
slope_end = 15
groove_count = 6
groove_width = 3
groove_depth = 2

# Create the sloped block
result = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (0, h_small),
        (slope_end, h_big),
        (length, h_big),
        (length, 0),
    ])
    .close()
    .extrude(depth)
)

# Compute groove center positions along X
positions = [
    slope_end + (length - slope_end) * (i + 1) / (groove_count + 1)
    for i in range(groove_count)
]
# Convert to workplane coordinates (origin at face center)
push_points = [(x - length / 2, 0) for x in positions]

# Cut grooves on the top face
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(push_points)
    .rect(groove_width, depth)
    .cutBlind(-groove_depth)
)