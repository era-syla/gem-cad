import cadquery as cq

handle = cq.Workplane("XY").box(30, 10, 5)
bowl = cq.Workplane("XY").workplane(offset=5).ellipse(15, 10).extrude(10).faces(">Z").workplane().ellipse(14, 9).cutThruAll()
result = handle.union(bowl)