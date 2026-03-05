import cadquery as cq

path = cq.Workplane("XZ").threePointArc((30, 50), (60, 0)).close()
profile = cq.Workplane("YZ").circle(5)
result = profile.sweep(path)

result