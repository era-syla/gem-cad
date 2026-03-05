import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(30, 60)
    .extrude(10)
    .edges("|Z")
    .fillet(5)
    .faces(">Z")
    .workplane()
    .circle(10)
    .extrude(20)
    .faces("<Z")
    .workplane(offset=-10)
    .circle(10)
    .extrude(-20)
)