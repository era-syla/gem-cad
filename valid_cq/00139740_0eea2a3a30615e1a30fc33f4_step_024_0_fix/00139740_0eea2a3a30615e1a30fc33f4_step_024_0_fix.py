import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(10)
    .extrude(100)
    .faces(">Z")
    .workplane()
    .circle(5)
    .cutBlind(-10)
    .faces("<Z")
    .workplane()
    .circle(5)
    .cutBlind(-10)
)