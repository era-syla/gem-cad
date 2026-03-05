import cadquery as cq

result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (20, 0), (30, 10), (60, 10),
               (60, 20), (30, 20), (20, 30), (0, 20)])
    .close()
    .extrude(5)
    .faces(">Z").workplane()
    .hole(5, 10)
    .center(10, 15).hole(5, 10)
    .center(15, -15).hole(5, 10)
    .center(15, 15).hole(5, 10)
    .edges("|Z").fillet(2)
)