import cadquery as cq

thread = cq.Workplane("XY").circle(3).extrude(50).faces(">Z").circle(4).cutThruAll()
head = cq.Workplane("XY").circle(6).extrude(2)
result = thread.union(head)