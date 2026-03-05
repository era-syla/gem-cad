import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(60, 20, 20)
    .edges()
    .fillet(2)
)