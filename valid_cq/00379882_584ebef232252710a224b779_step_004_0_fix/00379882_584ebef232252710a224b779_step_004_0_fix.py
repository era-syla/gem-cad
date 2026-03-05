import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(2)
    .extrude(1)
    .faces(">Z")
    .workplane()
    .rarray(4, 0, 4, 1)
    .circle(0.75)
    .cutThruAll()
    .faces(">Z")
    .workplane()
    .center(-18, 0)
    .rarray(3, 0, 10, 1)
    .circle(0.75)
    .cutThruAll()
)