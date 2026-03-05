import cadquery as cq

piston = cq.Workplane("XY").circle(12).extrude(20)
rod = cq.Workplane("XY").circle(3).extrude(30).translate((0, 0, 20))
crank_disk = cq.Workplane("YZ").circle(20).extrude(5)
pin_hole = cq.Workplane("XY", origin=(0, 0, 10)).circle(2).extrude(12)

crank_pin = cq.Workplane("XY").circle(3).extrude(3)
crank_assembly = crank_disk.cut(crank_pin)

piston_with_hole = piston.cut(pin_hole)

result = piston_with_hole.union(rod).union(crank_assembly)