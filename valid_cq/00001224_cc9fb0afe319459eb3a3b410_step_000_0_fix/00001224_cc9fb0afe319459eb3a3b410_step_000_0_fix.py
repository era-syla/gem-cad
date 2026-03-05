import cadquery as cq

pipe1 = cq.Workplane("front").circle(10).extrude(100)
pipe2 = cq.Workplane("front").circle(10).extrude(100).rotate((0, 0, 0), (0, 1, 0), 90).translate((50, 0, 0))

connector = (
    cq.Workplane("front")
    .circle(14)
    .extrude(10)
    .translate((50, 0, 50))
)

bend = (
    cq.Workplane("front")
    .threePointArc((50, 100, 0), (100, 100, 0))
    .circle(10)
    .sweep(cq.Workplane("front").line(100, 0).threePointArc((100, 100), (200, 100)))
)

result = pipe1.union(pipe2).union(connector).union(bend)