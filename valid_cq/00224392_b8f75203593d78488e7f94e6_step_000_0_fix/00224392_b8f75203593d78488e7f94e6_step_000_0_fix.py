import cadquery as cq

cylinder = cq.Workplane("XY").circle(10).extrude(50)
cutout = cq.Workplane("YZ").center(0, 10).rect(5, 50).extrude(5).translate((5, 0, 0))
result = cylinder.cut(cutout)