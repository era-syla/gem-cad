import cadquery as cq

result = (
    cq.Workplane("XY")
    .ellipse(30, 20)
    .extrude(10)
    .faces(">Z")
    .workplane()
    .rect(60, 40, forConstruction=True)
    .vertices()
    .circle(5)
    .cutThruAll()
)

result = (
    result
    .faces("<Z")
    .workplane()
    .hole(10, 2)
)