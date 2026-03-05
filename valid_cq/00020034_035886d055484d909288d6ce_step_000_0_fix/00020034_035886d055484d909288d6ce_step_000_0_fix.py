import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(50, 10, 5)
    .faces(">Z")
    .workplane()
    .rarray(20, 1, 2, 1)
    .rect(10, 5)
    .extrude(5)
    .faces("<Z")
    .workplane(offset=-5)
    .rarray(20, 1, 2, 1)
    .rect(5, 2)
    .cutBlind(-2)
)