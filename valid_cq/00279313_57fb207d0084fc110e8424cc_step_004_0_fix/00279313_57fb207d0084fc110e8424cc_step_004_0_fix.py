import cadquery as cq

result = cq.Workplane("XY").box(200, 40, 20)
result = result.faces(">Z").workplane().rect(180, 10).extrude(20, combine=False)
result = result.faces(">Z").workplane().rect(40, 10).extrude(20, combine=False)
result = result.faces(">Z").workplane().rect(80, 10).extrude(20, combine=False)
result = result.edges("|Z").fillet(1)