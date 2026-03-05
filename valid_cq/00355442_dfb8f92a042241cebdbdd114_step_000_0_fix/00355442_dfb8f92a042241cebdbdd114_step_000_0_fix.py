import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(3)
    .extrude(10)
    .faces(">Z")
    .workplane()
    .polarArray(4, 6, 360, 4)
    .circle(2)
    .cutThruAll()
)