import cadquery as cq

points = [(0, 0), (80, 0), (100, 10), (80, 20), (0, 20)]

result = (
    cq.Workplane("XY")
    .polyline(points).close().extrude(10)
    .faces(">Z").workplane().rect(10, 10).extrude(5)
    .faces(">Z").workplane().rect(20, 4).extrude(3)
    .faces(">Z")
    .workplane()
    .transformed(offset=(50, 10, 0))
    .text("NIKE", 8, 2, cut=True)
)