import cadquery as cq

L, W, T = 200, 20, 3

strap = (
    cq.Workplane("XY")
    .rect(L, W)
    .extrude(T)
    .edges().fillet(1)
    .faces(">Z")
    .workplane()
    .pushPoints([(-L/2+15, 0), (L/2-15, 0)])
    .hole(3)
)

resultMount = (
    strap
    .faces(">Z")
    .workplane()
    .circle(12.5).extrude(6)
    .faces(">Z").workplane().circle(12.5).extrude(2)
    .faces(">Z").workplane().circle(7.5).cutBlind(2)
)

block1 = (
    cq.Workplane("XY")
    .transformed(offset=(-50, 0, T))
    .rect(20, W-4)
    .extrude(6)
    .faces(">Z")
    .workplane()
    .pushPoints([(-5, 0), (5, 0)])
    .hole(3, 6)
)

block2 = (
    cq.Workplane("XY")
    .transformed(offset=(50, 0, T))
    .rect(20, W-4)
    .extrude(6)
    .faces(">Z")
    .workplane()
    .pushPoints([(-5, 0), (5, 0)])
    .hole(3, 6)
)

result = resultMount.union(block1).union(block2)