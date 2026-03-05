import cadquery as cq

rectangular_plate = cq.Workplane("XY").rect(10, 30).extrude(2)

long_hook = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(5, 0)
    .lineTo(5, 1)
    .threePointArc((2.5, 3.5), (0, 1))
    .close()
    .extrude(5)
)

short_hook = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(2.5, 0)
    .lineTo(2.5, 1)
    .threePointArc((1.25, 2), (0, 1))
    .close()
    .extrude(3)
)

connector = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(1, 0)
    .lineTo(1, 3)
    .lineTo(0, 3)
    .close()
    .extrude(2)
)

result = (
    rectangular_plate
    .union(connector.translate((0, 20, 0)))
    .union(long_hook.translate((0, 40, 0)))
    .union(short_hook.translate((0, 50, 0)))
)