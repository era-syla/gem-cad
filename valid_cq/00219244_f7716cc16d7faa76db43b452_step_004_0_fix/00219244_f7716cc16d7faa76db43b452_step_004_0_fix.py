import cadquery as cq

result = cq.Workplane("XY").rect(10, 10).extrude(10, both=False)
result = result.faces(">Z").workplane().moveTo(0, 5).lineTo(5, 0).lineTo(0, 0).close().cutBlind(-1)