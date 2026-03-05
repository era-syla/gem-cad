import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(20, 50)
    .extrude(5)
    .faces(">Z")
    .workplane(offset=10)
    .rect(20, 30)
    .extrude(5)
    .faces(">Z")
    .workplane(offset=-5)
    .move(0, 15)
    .rect(20, 10)
    .cutThruAll()
    .edges("|Z")
    .fillet(2)
)