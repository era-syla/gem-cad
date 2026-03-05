import cadquery as cq

profile = cq.Workplane("XY").moveTo(0, 0).lineTo(2, 4).lineTo(1, 4.5).lineTo(-1, 4.5).lineTo(-2, 4).close()
path = cq.Workplane("XZ").moveTo(0, 0).lineTo(0, 6)
result = profile.sweep(path)