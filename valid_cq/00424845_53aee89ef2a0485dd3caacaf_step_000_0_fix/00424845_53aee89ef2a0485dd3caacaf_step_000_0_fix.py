import cadquery as cq

# Hook part
hook = cq.Workplane("XY").circle(20).extrude(5)
hook = hook.faces(">Z").workplane().center(0,15).rect(8,10).extrude(-5)

# Pin part
pin = cq.Workplane("XY").circle(6).extrude(3)
pin = pin.faces(">Z").workplane().center(6,0).rect(4,2).extrude(3)
pin = pin.faces(">Z").workplane().circle(3).extrude(30)

result = hook.union(pin)