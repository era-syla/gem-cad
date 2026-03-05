import cadquery as cq

cylinder = cq.Workplane("XY").circle(50).extrude(10)
cutting_cylinder = cq.Workplane("XY").center(0, 0).circle(40).extrude(10)
arc_cut = cq.Workplane("XY").threePointArc((40, 20), (0, 40)).close().extrude(10)

result = cylinder.cut(cutting_cylinder).cut(arc_cut)