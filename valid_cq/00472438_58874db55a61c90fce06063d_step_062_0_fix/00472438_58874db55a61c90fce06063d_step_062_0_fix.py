import cadquery as cq

# Base block with pocket and holes
base = (
    cq.Workplane("XY")
    .box(40, 30, 30)
    .faces(">Y").workplane()
    .rect(12, 8).cutBlind(-4)
    .faces(">X").workplane()
    .pushPoints([(0, 10), (0, -10)]).hole(4)
    .pushPoints([(0, 0)]).hole(8)
)

# Top block with boss and hole
top = (
    cq.Workplane("XY")
    .workplane(offset=15)               # half height of base = 30/2 = 15
    .rect(20, 15).extrude(15)
    .faces(">Z").workplane()
    .rect(6, 6).extrude(10)
    .faces(">Z").workplane()
    .hole(3)
)

result = base.union(top)