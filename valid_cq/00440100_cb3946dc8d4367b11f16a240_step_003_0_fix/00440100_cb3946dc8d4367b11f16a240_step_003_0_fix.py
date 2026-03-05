import cadquery as cq

# Base
result = cq.Workplane("XY").rect(20, 40).extrude(80)

# Cutout in the base
cutout = cq.Workplane("XY").rect(10, 30).extrude(70)
result = result.cut(cutout)

# Top extension
result = result.faces(">Z").workplane().rect(12, 12).extrude(20)

# Small cylinder on top
result = result.faces(">Z").workplane().circle(4).extrude(10)

# Hole through the cylinder
result = result.faces(">Z").workplane(centerOption='CenterOfBoundBox').circle(1).cutBlind(-10)