import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(10).extrude(5)
    .faces(">Z").workplane()
    .center(-10, 0).circle(5).cutBlind(-5)
    .center(20, 0).circle(5).cutBlind(-5)
)