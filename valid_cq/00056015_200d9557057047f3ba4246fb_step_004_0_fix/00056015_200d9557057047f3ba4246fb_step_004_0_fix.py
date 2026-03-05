import cadquery as cq

# Base plate
plate = cq.Workplane("XY").box(60, 20, 3)

# Circular hole through the plate
plate = plate.faces(">Z").workplane().center(-15, 0).circle(3).cutThruAll()

# Four prongs at one end
y_positions = [-4.5, -1.5, 1.5, 4.5]
prongs = (
    cq.Workplane("XY")
    .transformed(offset=(-25, 0, 3))
    .pushPoints([(0, y) for y in y_positions])
    .rect(1, 1)
    .extrude(10)
)

# Small block next to the hole
block1 = (
    cq.Workplane("XY")
    .transformed(offset=(-13, 0, 3))
    .rect(4, 3)
    .extrude(5)
)

# Mid-sized block on the plate
block2 = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 3))
    .rect(10, 5)
    .extrude(2)
)

# Two tall posts at the opposite end
post1 = (
    cq.Workplane("XY")
    .transformed(offset=(25, 5, 3))
    .rect(6, 10)
    .extrude(20)
)
post2 = (
    cq.Workplane("XY")
    .transformed(offset=(25, -5, 3))
    .rect(6, 10)
    .extrude(20)
)

# Combine all parts into the final result
result = plate.union(prongs).union(block1).union(block2).union(post1).union(post2)