import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(20, 40, 10)
    .edges("|Z")
    .fillet(5)
    .faces(">Z")
    .workplane()
    .pushPoints([(-6, -6), (6, -6), (-6, 6), (6, 6)])
    .hole(2)
)