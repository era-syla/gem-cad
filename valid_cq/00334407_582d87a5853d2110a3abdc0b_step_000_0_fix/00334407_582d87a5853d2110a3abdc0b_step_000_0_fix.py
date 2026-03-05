import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(10)
    .extrude(5)
    .faces(">Z")
    .workplane()
    .circle(5)
    .cutThruAll()
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .rect(20, 5)
    .extrude(5)
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .rect(5, 30)
    .extrude(20)
)