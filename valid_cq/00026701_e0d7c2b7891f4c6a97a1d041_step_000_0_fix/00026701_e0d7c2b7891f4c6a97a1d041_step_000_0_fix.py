import cadquery as cq

base = cq.Workplane("XY").box(60, 40, 10)

cut1 = cq.Workplane("XY", origin=(0, 0, 5)).circle(5).cutThruAll()
cut2 = cq.Workplane("XY", origin=(0, 0, 5)).rect(10, 10).cutThruAll()

arm1 = cq.Workplane("XY", origin=(30, 0, 0)).box(40, 10, 10)
arm2 = cq.Workplane("XY", origin=(-30, 0, 0)).box(40, 10, 10)

sphere = cq.Workplane("XY", origin=(0, 0, 25)).sphere(5)

result = base.union(arm1).union(arm2).cut(cut1).cut(cut2).union(sphere)