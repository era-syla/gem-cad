import cadquery as cq

bolt_head = cq.Workplane("XY").circle(5).extrude(2)
shank = cq.Workplane("XY").circle(3).extrude(30)
thread = cq.Workplane("XY").circle(3.5).extrude(20)

bolt = bolt_head.union(shank.translate((0, 0, 2))).union(thread.translate((0, 0, 10)))

result = bolt