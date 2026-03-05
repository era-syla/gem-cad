import cadquery as cq

hex_head = cq.Workplane("XY").polygon(6, 10).extrude(4)
cylinder_shaft = cq.Workplane("XY").circle(3).extrude(25)
screw_thread = cq.Workplane("XY").circle(3.5).extrude(12)
thread = cq.Workplane("YZ").workplane(offset=29).circle(3.5).sweep(cq.Workplane("YZ").lineTo(-12, 0))

result = hex_head.union(cylinder_shaft).union(thread)