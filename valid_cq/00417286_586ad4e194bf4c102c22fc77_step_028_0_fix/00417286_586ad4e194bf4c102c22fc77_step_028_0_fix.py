import cadquery as cq

result = (
    cq.Workplane("XY")
    .center(0, 0)
    .threePointArc((30, 60), (100, 0))
    .lineTo(70, 0)
    .threePointArc((30, -60), (0, 0))
    .close()
    .extrude(5)
    .faces(">Z").workplane()
    .pushPoints([(-75, 0), (-45, 0), (-15, 0), (15, 0), (45, 0), (75, 0)])
    .hole(5)
    .faces("<Z").workplane()
    .rect(140, 10)
    .vertices()
    .hole(5)
)