import cadquery as cq

result = (
    cq.Workplane("XY")
    .lineTo(50, 0)
    .threePointArc((55, 5), (50, 10))
    .lineTo(0, 10)
    .threePointArc((-5, 5), (0, 0))
    .close()
    .extrude(2)
)