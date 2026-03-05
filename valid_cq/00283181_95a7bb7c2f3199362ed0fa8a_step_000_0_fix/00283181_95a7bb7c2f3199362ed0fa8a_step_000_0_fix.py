import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(15).extrude(5)
    .circle(20).extrude(10)
    .circle(18).extrude(15)
    .circle(22).extrude(5)
    .circle(20).extrude(10)
    .circle(22).extrude(5)
    .circle(25).extrude(10)
)