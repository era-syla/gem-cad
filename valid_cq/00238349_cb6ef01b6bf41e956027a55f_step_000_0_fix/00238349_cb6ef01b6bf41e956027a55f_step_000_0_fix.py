import cadquery as cq

path = cq.Workplane("XZ").moveTo(0, 0).lineTo(0, 20).threePointArc((10, 30), (20, 20))
profile = cq.Workplane("XY").circle(5)

result = profile.sweep(path)