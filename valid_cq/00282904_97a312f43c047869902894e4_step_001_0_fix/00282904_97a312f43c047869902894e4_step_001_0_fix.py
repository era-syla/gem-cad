import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(10, 100)
    .extrude(10)
    .faces(">Z")
    .workplane()
    .rect(10, 50, forConstruction=True)
    .vertices()
    .hole(3)
    .faces(">Z")
    .workplane()
    .text("3D Industries", 5, 0.2, combine=False)
)