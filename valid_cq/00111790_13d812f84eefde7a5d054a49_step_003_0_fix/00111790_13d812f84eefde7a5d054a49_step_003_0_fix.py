import cadquery as cq

result = (
    cq.Workplane("XY")
    .lineTo(30, 0)
    .lineTo(50, -10)
    .lineTo(60, -40)
    .lineTo(30, -30)
    .lineTo(0, -40)
    .close()
    .extrude(5)
    .faces(">Z")
    .workplane()
    .center(45, -5)
    .circle(5)
    .cutThruAll()
)

result = result.edges().fillet(2)