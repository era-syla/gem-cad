import cadquery as cq
import math

R = 10
thickness = 5

result = (
    cq.Workplane("XZ")
    .moveTo(R, 0)
    .threePointArc((R/math.sqrt(2), R/math.sqrt(2)), (0, R))
    .lineTo(0, 0)
    .close()
    .extrude(thickness)
)