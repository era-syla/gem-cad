import cadquery as cq

result = (
    cq.Workplane("XY")
    .moveTo(-60, 0)
    .lineTo(0, 0)
    .threePointArc((3, 25), (0, 50))
    .lineTo(-60, 50)
    .close()
    .extrude(5)
)