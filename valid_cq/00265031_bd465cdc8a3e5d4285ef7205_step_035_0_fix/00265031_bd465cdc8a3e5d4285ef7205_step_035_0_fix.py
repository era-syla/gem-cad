import cadquery as cq

male = (
    cq.Workplane("XY")
    .box(60, 20, 10)
    .faces(">Z")
    .workplane()
    .pushPoints([(25, -5), (25, 5)])
    .rect(4, 8)
    .extrude(4)
)

female = (
    cq.Workplane("XY")
    .box(60, 20, 10)
    .faces(">Z")
    .workplane()
    .pushPoints([(-25, -5), (-25, 5)])
    .rect(4, 8)
    .cutThruAll()
    .translate((70, 0, 0))
)

result = male.union(female)