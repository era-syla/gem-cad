import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(200, 20)
    .extrude(5)
    .edges("|Z")
    .fillet(2.5)
    .faces(">Z")
    .workplane()
    .rect(180, 5)
    .cutThruAll()
    .faces(">Z")
    .workplane(offset=-10)
    .hole(3)
)