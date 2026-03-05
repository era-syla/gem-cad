import cadquery as cq

result = (
    cq.Workplane("XY")
    .center(10, 0)
    .circle(7.5)
    .center(-20, 0)
    .circle(7.5)
    .center(10, 0)
    .rect(20, 40)
    .extrude(3)
    .faces(">Z").workplane()
    .hole(5)
    .center(-10, 10).hole(5)
    .center(20, 0).hole(5)
)