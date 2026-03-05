import cadquery as cq

fuselage = cq.Workplane("XY").rect(100, 5).extrude(6).translate((0, 0, -3))
wing = cq.Workplane("XY").rect(200, 20).extrude(2).translate((0, 0, 3))
ht = cq.Workplane("XY").rect(40, 8).extrude(2).translate((50, 0, 3))
vt = cq.Workplane("XZ").rect(10, 25).extrude(5, both=True).translate((50, 0, 15.5))

result = fuselage.union(wing).union(ht).union(vt)