import cadquery as cq

outer_circle = cq.Workplane("XY").circle(30).extrude(10, both=True)
inner_circle = cq.Workplane("XY").circle(25).extrude(10, both=True)
cylinder = outer_circle.cut(inner_circle)

arm = cq.Workplane("XY").rect(100, 10).extrude(5).translate((50, 0, 0))

hole_arm = arm.faces("<Z").workplane().hole(6).faces(">Z").hole(6)

result = cylinder.union(hole_arm)