import cadquery as cq

outer_ring = (
    cq.Workplane("XY")
    .circle(15)
    .extrude(5)
)

inner_cutout = (
    cq.Workplane("XY")
    .circle(10)
    .extrude(5)
)

ring = outer_ring.cut(inner_cutout)

triangle_part = (
    cq.Workplane("XY")
    .moveTo(-15, 0)
    .lineTo(0, 30)
    .lineTo(20, 0)
    .close()
    .extrude(5)
)

hole = (
    cq.Workplane("XY")
    .workplane(offset=2.5)
    .moveTo(10, 0)
    .circle(2.5)
    .extrude(5, combine=False)
)

result = ring.union(triangle_part).cut(hole)
