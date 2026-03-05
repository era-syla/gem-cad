import cadquery as cq

# Create a stepped rod
rod = (
    cq.Workplane("XY")
    .circle(2).extrude(80)
    .faces(">Z").workplane()
    .circle(3).extrude(2)
    .faces(">Z").workplane()
    .circle(2).extrude(10)
)

# Position two rods
rod1 = rod.translate((0, -5, 0))
rod2 = rod.translate((0, 5, 0))

# Create the larger mounting block with two holes
block2 = (
    cq.Workplane("XY")
    .workplane(offset=20)
    .box(40, 10, 6)
    .faces(">Z")
    .workplane()
    .pushPoints([(-8, 0), (8, 0)])
    .hole(4)
)

# Create the smaller mounting block with two holes
block1 = (
    cq.Workplane("XY")
    .workplane(offset=30)
    .box(20, 8, 4)
    .faces(">Z")
    .workplane()
    .pushPoints([(-4, 0), (4, 0)])
    .hole(4)
)

# Create the top lever piece
lever = (
    cq.Workplane("XY")
    .workplane(offset=36)
    .rect(12, 5)
    .extrude(4)
    .faces(">Z")
    .workplane()
    .pushPoints([(5.5, 0)])
    .circle(2)
    .extrude(6)
)

# Combine all parts into the final result
result = rod1.union(rod2).union(block2).union(block1).union(lever)