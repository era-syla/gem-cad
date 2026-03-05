import cadquery as cq

result = (
    cq.Workplane("XY")
    .ellipse(20, 10)
    .extrude(5)
    .workplane(offset=5)
    .ellipse(20, 10).extrude(3)
)