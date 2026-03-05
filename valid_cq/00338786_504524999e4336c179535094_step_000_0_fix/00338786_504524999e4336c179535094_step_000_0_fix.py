import cadquery as cq

part1 = cq.Workplane("XY").polyline([(0, 0), (5, 0), (5, 10), (2, 10), (2, 2), (0, 2)]).close().extrude(3).translate((-80, 0, 0))
part2 = cq.Workplane("XY").box(15, 8, 2).translate((-60, 0, 0))
part3 = cq.Workplane("XZ").circle(1).extrude(8).translate((-40, 0, 1))
part4 = cq.Workplane("XY").box(18, 8, 2).translate((-20, 0, 0))
part5 = cq.Workplane("XZ").circle(1).extrude(8).translate((0, 0, 1))
part6 = cq.Workplane("XY").box(16, 2, 2).union(cq.Workplane("XY").box(2, 16, 2)).translate((20, 0, 0))
part7 = cq.Workplane("XY").box(10, 6, 2).translate((40, 0, 0))
part8 = cq.Workplane("XY").polyline([(0, 0), (8, 0), (8, 1), (1, 1), (1, 8), (0, 8)]).close().extrude(3).translate((60, 0, 0))
wrench = cq.Workplane("XY").box(8, 2, 1).union(cq.Workplane("XY").box(2, 8, 1)).translate((80, 0, 0))

result = part1.union(part2).union(part3).union(part4).union(part5).union(part6).union(part7).union(part8).union(wrench)