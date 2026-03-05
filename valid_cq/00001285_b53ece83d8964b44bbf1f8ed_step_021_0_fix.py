import cadquery as cq

result = (
    cq.Workplane("XY")
    .circle(20)
    .circle(10)
    .extrude(3)
)