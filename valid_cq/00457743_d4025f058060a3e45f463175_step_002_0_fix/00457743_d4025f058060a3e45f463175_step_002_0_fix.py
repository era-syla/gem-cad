import cadquery as cq

result = cq.Workplane("XY").cylinder(60, 15).faces(">Z").workplane().cylinder(30, 10)

result = result.faces(">Z").workplane().hole(2)