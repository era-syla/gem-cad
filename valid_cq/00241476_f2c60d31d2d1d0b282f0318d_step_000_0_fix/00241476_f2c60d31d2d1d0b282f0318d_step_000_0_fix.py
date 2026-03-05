import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(20)
    .extrude(5)
    .faces(">Z").workplane()
    .circle(5).extrude(-5)
    .faces("<Z").workplane()
    .center(30, 0).circle(5).extrude(5)
    .center(-60, 0).circle(5).extrude(5)
)