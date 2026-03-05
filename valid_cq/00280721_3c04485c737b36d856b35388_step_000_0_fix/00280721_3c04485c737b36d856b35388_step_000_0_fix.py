import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(5).extrude(10)
    .faces(">Z").workplane()
    .circle(3).extrude(10)
    .faces(">Z").workplane()
    .circle(5).extrude(10)
)