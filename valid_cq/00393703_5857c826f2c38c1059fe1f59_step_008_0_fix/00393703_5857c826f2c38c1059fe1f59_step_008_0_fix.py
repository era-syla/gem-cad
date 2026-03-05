import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(50, 60, 10)
    .faces(">Z").workplane()
    .rect(40, 50, centered=False)
    .cutBlind(-5)
    .faces(">Z").workplane()
    .rect(10, 10, centered=False)
    .cutBlind(-10)
    .faces(">Y").workplane()
    .rect(10, 30, centered=False)
    .extrude(10)
    .faces("<X").workplane()
    .rect(30, 10, centered=False)
    .cutBlind(-5)
)
