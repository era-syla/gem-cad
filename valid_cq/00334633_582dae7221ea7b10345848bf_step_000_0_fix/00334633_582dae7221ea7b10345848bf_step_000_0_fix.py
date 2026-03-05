import cadquery as cq

# Parameters
thickness = 5
hole_diameter = 6

# 2D profile points (in mm)
profile = [
    (0, 0),
    (40, 0),
    (50, 10),
    (50, 50),
    (30, 80),
    (20, 80),
    (0, 60)
]

# Hole positions on the top face
hole_positions = [
    (40, 0),
    (45, 5),
    (50, 30),
    (40, 65),
    (25, 80)
]

# Build the bracket
result = (
    cq.Workplane("XY")
    .polyline(profile)
    .close()
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, thickness)
)