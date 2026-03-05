import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(60, 20, 10)
    .faces(">Z").workplane()
        .rect(50, 15).extrude(5)
    .edges("|Z").chamfer(2)
    .faces(">Z").workplane()
        .pushPoints([(0, 7.5), (0, -7.5)])
        .rect(50, 1).cutBlind(-1)
    .faces(">Z").workplane()
        .hole(6)
    .faces(">Z").workplane()
        .circle(6).cutBlind(-2)
)