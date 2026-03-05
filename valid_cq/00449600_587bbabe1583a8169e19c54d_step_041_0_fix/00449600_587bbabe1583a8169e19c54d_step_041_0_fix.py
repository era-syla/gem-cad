import cadquery as cq

# Parameters
plateHeight = 80
plateThickness = 3
topHeight = 15
rodRadius = 1.5
rodExtension = 5
slotWidth = 6
slotDepth = 8
plateWidth = 10
holeDia = 4
holePositions = [(0, -20), (0, -40)]

# Rod
rodLength = plateHeight + topHeight + 2 * rodExtension
rod = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, -rodExtension))
    .circle(rodRadius)
    .extrude(rodLength)
)

# Top extrusion
top = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, plateHeight))
    .rect(20, 20)
    .extrude(topHeight)
)

# Cut T‐slots on the top
slotCenters = [
    (0, 10 - slotDepth / 2),
    (0, -10 + slotDepth / 2),
    (10 - slotDepth / 2, 0),
    (-10 + slotDepth / 2, 0),
]
for x, y in slotCenters:
    a, b = (slotWidth, slotDepth) if abs(y) > 0.1 else (slotDepth, slotWidth)
    slot = (
        cq.Workplane("XY")
        .transformed(offset=(x, y, plateHeight + topHeight / 2))
        .rect(a, b)
        .extrude(topHeight + 1)
    )
    top = top.cut(slot)

# Plate beneath top
plate = (
    cq.Workplane("XY")
    .rect(plateWidth, plateHeight)
    .extrude(-plateThickness)
    .faces(">Z")
    .workplane()
    .pushPoints(holePositions)
    .hole(holeDia, plateThickness + 1)
)

# Combine all parts
result = rod.union(top).union(plate)