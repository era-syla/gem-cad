import cadquery as cq

path = cq.Workplane("XZ").threePointArc((15, 15), (30, 0))
result = cq.Workplane("XY").circle(5).sweep(path)

result