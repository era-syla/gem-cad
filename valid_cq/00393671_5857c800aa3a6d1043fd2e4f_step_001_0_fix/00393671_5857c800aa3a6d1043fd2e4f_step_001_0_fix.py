import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(80, 15, 10, centered=(False, True, False))
    # top slot
    .faces(">Z").workplane()
    .rect(50, 3)
    .cutBlind(-1)
    # side pocket
    .faces(">Y").workplane()
    .polyline([(20, 2), (40, 5), (40, 1), (20, 1)])
    .close()
    .cutBlind(1)
    # front protrusion
    .faces("<X").workplane()
    .rect(8, 6)
    .extrude(10)
    # back ramp cut
    .faces(">Y").workplane()
    .polyline([(60, 10), (80, 0), (80, 10)])
    .close()
    .cutThruAll()
)