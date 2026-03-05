import cadquery as cq

result = cq.Workplane("XY").rect(10, 10).extrude(100).edges("|Z").fillet(1)