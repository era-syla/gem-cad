import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(60, 60)
    .extrude(10)
    .faces(">Z")
    .workplane()
    .circle(15)
    .cutThruAll()
    .faces(">Z")
    .workplane()
    .rarray(40, 40, 2, 2)
    .circle(5)
    .cutThruAll()
)