import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(50, 50, 10)
    .faces(">Z")
    .workplane()
    .rect(20, 20)
    .cutBlind(-5)
    .faces(">Z")
    .workplane()
    .polygon(12, 10)
    .cutBlind(-7)
    .workplane(offset=-10)
    .circle(15)
    .cutThruAll()
    .edges()
    .fillet(1)
)