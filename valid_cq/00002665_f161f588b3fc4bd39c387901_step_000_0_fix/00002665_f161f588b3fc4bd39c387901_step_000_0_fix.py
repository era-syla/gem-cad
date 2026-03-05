import cadquery as cq

base = cq.Workplane("XY").box(60, 20, 10).edges("|Z").fillet(5)
pillar = cq.Workplane("XY").workplane(offset=10).circle(7.5).extrude(30)
holder = cq.Workplane("XY").workplane(offset=40).circle(12).extrude(8).faces(">Z").workplane().hole(10)
cutout = (cq.Workplane("XY").workplane(offset=48).rect(20, 8).extrude(-8))

result = base.union(pillar).union(holder).cut(cutout)