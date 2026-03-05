import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(50, 50, 10)
    .workplane(offset=10)
    .rect(30, 30)
    .cutBlind(-10)
    .edges("|Z")
    .fillet(5)
)