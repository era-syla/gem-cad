import cadquery as cq

profile = cq.Workplane("XY").rect(2, 0.5).extrude(100)
result = profile.faces(">Z").edges().fillet(0.1)