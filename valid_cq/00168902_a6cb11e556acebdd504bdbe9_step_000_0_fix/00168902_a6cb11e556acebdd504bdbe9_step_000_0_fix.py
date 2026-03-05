import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(1.5)
    .extrude(2)
    .faces(">Z")
    .workplane()
    .circle(0.5)
    .extrude(20)
    .faces(">Z")
    .workplane()
    .circle(2)
    .sphere(4)
)