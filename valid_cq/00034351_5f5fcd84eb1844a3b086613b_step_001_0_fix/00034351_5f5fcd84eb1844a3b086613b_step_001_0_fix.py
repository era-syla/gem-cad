import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(60, 10, 2)
    .faces(">Z")
    .workplane()
    .rarray(10, 1, 6, 1)
    .circle(2)
    .extrude(8)
    .edges("|Z")
    .fillet(1)
)
