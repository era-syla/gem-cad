import cadquery as cq

plate = (
    cq.Workplane("XY")
    .box(120, 80, 2)
    .faces(">Z").workplane()
    .circle(5).cutThruAll()
    .center(40, 0).circle(5).cutThruAll()
    .center(-80, 0).circle(5).cutThruAll()
    .center(40, 0).rect(20, 10).cutThruAll()
    .center(-40, -30).rect(15, 10).cutThruAll()
)

panel = (
    cq.Workplane("XY")
    .box(60, 40, 2)
    .faces(">Z").workplane()
    .rect(30, 20).cutThruAll()
    .center(0, 15).rect(20, 10).cutThruAll()
    .center(0, -30).rect(40, 5).cutThruAll()
)

result = plate.union(panel)