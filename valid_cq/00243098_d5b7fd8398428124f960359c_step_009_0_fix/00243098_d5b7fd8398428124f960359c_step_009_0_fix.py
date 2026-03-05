import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(70, 140, 7)
    .edges("|Z").fillet(5)
    .faces(">Z").workplane()
    .rect(60, 120).cutThruAll()
    .faces(">Z").workplane(offset=-3)
    .rect(120, 10).cutBlind(-2)
    .faces("<Z").workplane()
    .move(0, 50).circle(5).cutThruAll()
    .edges("%Circle").fillet(1)
)