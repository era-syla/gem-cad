import cadquery as cq

base = cq.Workplane().circle(10).extrude(100)
flange = (
    cq.Workplane("XZ")
    .transformed(offset=(0, 0, 100))
    .moveTo(-15, -5)
    .lineTo(15, -5)
    .radiusArc((20, 0), 5)
    .lineTo(20, 10)
    .lineTo(-20, 10)
    .close()
    .extrude(5)
)
result = base.union(flange)