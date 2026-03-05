import cadquery as cq

points = [
    (0, 0),
    (5, 0),
    (5, 100),
    (7, 102),
    (6, 104),
    (7, 106),
    (4, 110),
    (4, 130),
    (1.5, 145),
    (0, 150),
]

result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(0, 0, 1))
)