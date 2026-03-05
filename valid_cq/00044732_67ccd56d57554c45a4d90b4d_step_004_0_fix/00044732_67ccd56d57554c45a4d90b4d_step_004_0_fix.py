import cadquery as cq

result = (
    cq.Workplane("XY")
    .polyline([(0, 20), (100, 5), (100, -5), (0, -20)])
    .close()
    .extrude(5)
    .faces(">Z")
    .workplane()
    .center(95, 0)
    .hole(6)
    .faces(">Z")
    .workplane()
    .circle(15)
    .extrude(40)
    .faces(">Z")
    .workplane()
    .circle(13)
    .cutBlind(-40)
)

nut1 = (
    cq.Workplane("YZ", origin=(15, 0, 20))
    .polygon(6, 12)
    .extrude(5)
    .faces(">X")
    .workplane()
    .hole(6)
)

nut2 = (
    cq.Workplane("YZ", origin=(15, 0, 30))
    .polygon(6, 12)
    .extrude(5)
    .faces(">X")
    .workplane()
    .hole(6)
)

result = result.union(nut1).union(nut2)