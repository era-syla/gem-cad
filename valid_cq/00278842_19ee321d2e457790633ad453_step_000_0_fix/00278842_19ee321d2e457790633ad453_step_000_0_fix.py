import cadquery as cq

result = (
    cq.Workplane("XY")
    .moveTo(-30, 0)
    .lineTo(-10, 0)
    .threePointArc((0, 10), (10, 0))
    .lineTo(30, 0)
    .lineTo(30, -10)
    .lineTo(10, -10)
    .threePointArc((0, -20), (-10, -10))
    .lineTo(-30, -10)
    .close()
    .extrude(5)
)