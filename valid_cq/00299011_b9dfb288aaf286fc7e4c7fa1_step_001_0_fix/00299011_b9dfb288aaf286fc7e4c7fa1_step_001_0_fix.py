import cadquery as cq

cylinder = cq.Workplane("XY").circle(5).extrude(40)
legs = (
    cq.Workplane("XY")
    .circle(1.5)
    .extrude(60)
    .translate((7, 0, 0))
    .union(
        cq.Workplane("XY")
        .circle(1.5)
        .extrude(60)
        .translate((0, 7, 0))
    )
    .union(
        cq.Workplane("XY")
        .circle(1.5)
        .extrude(60)
        .translate((-7, 0, 0))
    )
    .union(
        cq.Workplane("XY")
        .circle(1.5)
        .extrude(60)
        .translate((0, -7, 0))
    )
)
result = cylinder.union(legs.translate((0, 0, 40)))