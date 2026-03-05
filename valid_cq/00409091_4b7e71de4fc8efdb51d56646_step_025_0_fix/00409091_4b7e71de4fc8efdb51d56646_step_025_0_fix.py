import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(60, 30, 15)
    .faces(">Z").workplane()
    .hole(10)
    .workplane(offset=-5)
    .hole(8)
    .faces("<Z").workplane()
    .lineTo(30, 0).lineTo(30, 15).lineTo(0, 15).close()
    .extrude(3)
)