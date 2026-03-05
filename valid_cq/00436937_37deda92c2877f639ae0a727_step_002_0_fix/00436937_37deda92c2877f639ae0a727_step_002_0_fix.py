import cadquery as cq

base = cq.Workplane("XY").circle(20).extrude(5)
cylinders = (
    base.faces(">Z")
    .workplane()
    .rarray(40, 40, 2, 2)
    .circle(5)
    .extrude(15)
)

handle = (
    base.faces(">Z")
    .workplane(offset=15)
    .center(0, 25)
    .rect(5, 40)
    .extrude(5)
)

oval = (
    handle.faces(">Z")
    .workplane()
    .center(0, 10)
    .ellipse(20, 10)
    .cutThruAll()
)

result = handle.union(cylinders).union(base.union(oval))