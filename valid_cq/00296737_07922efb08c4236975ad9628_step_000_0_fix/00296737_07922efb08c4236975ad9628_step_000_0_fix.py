import cadquery as cq

profile = [
    (0, 0),
    (10, 0),
    (10, 40),
    (8, 50),
    (7, 70),
    (5, 80),
    (5, 90),
    (0, 90),
]

result = cq.Workplane("XZ").polyline(profile).close().revolve()