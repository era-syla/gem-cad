import cadquery as cq

thickness = 5
points = [(0, 0), (120, 0), (220, 80), (170, 180), (0, 140)]

result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

hole_positions = [
    (0, 0),
    (120, 0),
    (220, 80),
    (170, 180),
    (0, 140),
    (60, 40),
    (140, 100),
    (180, 140),
    (180, 30),
    (70, 110),
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(6)
    .edges()
    .fillet(2)
)