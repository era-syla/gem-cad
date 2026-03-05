import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(80, 30, 35, centered=(True, True, False))
    .edges("|Z")
    .fillet(2)
    .edges(">Z")
    .fillet(8)
)