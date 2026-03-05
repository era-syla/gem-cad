import cadquery as cq

# Base
base = cq.Workplane("XY").circle(10).extrude(20)

# Legs
legs = (
    cq.Workplane("XY")
    .circle(1.5)
    .extrude(30)
    .translate((0, -5, -30))
    .polarArray(0, 0, 360, 3)
    .cut(cq.Workplane("XY").rect(3, 1.5).extrude(35).translate((0, 0, -5)))
)

# Top support
support = (
    cq.Workplane("XY")
    .polygon(3, 8)
    .extrude(3)
    .translate((0, 0, 20))
)

# Join parts
result = base.union(legs).union(support)