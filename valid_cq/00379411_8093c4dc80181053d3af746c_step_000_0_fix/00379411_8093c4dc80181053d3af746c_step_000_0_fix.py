import cadquery as cq

result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (10, 0), (12, 2), (10, 4), (6, 4), (4, 6), (2, 4), (0, 4)])
    .close()
    .extrude(2)
)