import cadquery as cq

result = (
    cq.Workplane("XY")
    .polygon(6, 100)
    .workplane(offset=-20)
    .circle(10)
    .loft(combine=True)
)

result = result.cut(
    cq.Workplane("XY").circle(20).extrude(-20)
)