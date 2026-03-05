import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(12)
    .extrude(4)
    .faces(">Z")
    .vertices()
    .circle(4)
    .cutThruAll()
    .faces(">Z")
    .workplane(offset=6)
    .circle(8)
    .extrude(4)
    .faces(">Z")
    .vertices()
    .circle(4)
    .cutThruAll()
)