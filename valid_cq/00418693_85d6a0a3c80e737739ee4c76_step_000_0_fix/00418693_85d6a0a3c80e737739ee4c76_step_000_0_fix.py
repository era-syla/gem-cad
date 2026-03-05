import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(40, 60)
    .extrude(3)
    .faces(">Z").workplane()
    .rect(30, 50)
    .cutBlind(-3)
    .faces(">Z").workplane()
    .circle(3).cutBlind(-3)
    .faces(">Z").workplane(offset=20)
    .pushPoints([(-15,0), (15,0)])
    .circle(2).cutBlind(-5)
    .edges().fillet(1)
)