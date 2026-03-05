import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(100, 60)
    .extrude(5)
    .edges("|Z").fillet(3)
    .faces(">Z")
    .workplane()
    .center(-30, 20)
    .slot2D(10, 2.5)
    .cutBlind(5)
    .center(60, 0)
    .slot2D(10, 2.5)
    .cutBlind(5)
)