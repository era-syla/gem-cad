import cadquery as cq

length = 100
diameter = 10

result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(length)
)