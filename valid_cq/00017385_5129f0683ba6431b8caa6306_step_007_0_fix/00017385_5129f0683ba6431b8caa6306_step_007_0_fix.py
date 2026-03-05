import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(20, 40)
    .extrude(10)
    .faces(">Z")
    .workplane()
    .circle(5)
    .extrude(-10)
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .circle(5)
    .extrude(-10)
)