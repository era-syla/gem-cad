import cadquery as cq

result = cq.Workplane("XY").box(20, 50, 10)

result = result.faces(">Z").workplane().sphere(5)

result = result.faces("<Z").workplane().circle(4).workplane(offset=-15).circle(2).loft(combine=True)

result = result.faces("<Z").workplane().circle(3).cutThruAll()
