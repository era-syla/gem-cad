import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(5)
    .extrude(20)
    .faces(">Z")
    .circle(3)
    .extrude(15)
    .faces(">Z")
    .sphere(3)
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .circle(4)
    .cutBlind(-3)
)