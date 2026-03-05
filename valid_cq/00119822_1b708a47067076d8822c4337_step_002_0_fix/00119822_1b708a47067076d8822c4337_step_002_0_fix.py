import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(60, 10)
    .extrude(5)
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .rarray(50, 1, 2, 1)
    .circle(4)
    .cutThruAll()
)