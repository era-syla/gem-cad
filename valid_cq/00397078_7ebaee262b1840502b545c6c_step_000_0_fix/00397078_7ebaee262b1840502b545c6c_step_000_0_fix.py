import cadquery as cq

# Create the outer bottle shape by lofting circles at different heights and offsets
outer = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(10)
    .workplane(offset=30)
    .center(2, 0)
    .circle(9)
    .workplane(offset=60)
    .center(-1, 0)
    .circle(8)
    .workplane(offset=90)
    .center(0, 0)
    .circle(6)
    .workplane(offset=110)
    .center(0, 0)
    .circle(5)
    .loft(combine=True)
)

# Add the cylindrical neck
outer = outer.union(
    cq.Workplane("XY")
    .workplane(offset=110)
    .center(0, 0)
    .circle(5)
    .extrude(20)
)

# Hollow out the interior
outer = outer.cut(
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(4)
    .extrude(140)
)

result = outer