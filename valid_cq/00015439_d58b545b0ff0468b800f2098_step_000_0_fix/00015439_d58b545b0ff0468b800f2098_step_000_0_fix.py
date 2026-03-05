import cadquery as cq

result = (cq.Workplane("XY")
    .circle(15).extrude(20)
    .faces(">Z").workplane()
    .rect(30, 60).extrude(-10)
    .faces(">Z[1]").workplane()
    .circle(5).cutBlind(-20))