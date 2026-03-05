import cadquery as cq

# Create the main body
result = cq.Workplane("XY").polygon(3, 100).extrude(10)

# Create cutout
cutout = cq.Workplane("XY").polygon(3, 85).extrude(10)
result = result.cut(cutout)

# Create small holes
result = result.faces(">Z").workplane().pushPoints([(-20, 0), (20, 0)]).circle(3).cutThruAll()

# Create the slot
slot_shape = cq.Workplane("XY").circle(10).extrude(10)
slot_shape = slot_shape.faces(">Z").workplane().rect(20, 10).cutThruAll()
result = result.cut(slot_shape.translate((0, 50, 0)))