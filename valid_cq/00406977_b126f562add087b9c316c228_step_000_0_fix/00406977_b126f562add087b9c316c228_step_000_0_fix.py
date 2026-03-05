import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(60, 10, 5)
    .edges("|X").fillet(1)
    .faces(">Z").workplane()
    .rect(50, 4)
    .cutThruAll()
    .faces("<Z").workplane(offset=-5)
    .center(-20, 0)
    .rect(10, 4)
    .extrude(5)
    .faces(">Z").workplane()
    .center(15, 0)
    .rect(5, 4)
    .extrude(5)
)