import cadquery as cq

cylinder = cq.Workplane("XY").circle(10).extrude(20)

helix_path = cq.Workplane("XY").moveTo(5, 0).threePointArc((10, 0), (0, -20))

spirals = cq.Workplane("XY").polygon(3, 12).sweep(helix_path.rotate((0, 0, 0), (0, 0, 1), 120))

result = cylinder.cut(spirals)