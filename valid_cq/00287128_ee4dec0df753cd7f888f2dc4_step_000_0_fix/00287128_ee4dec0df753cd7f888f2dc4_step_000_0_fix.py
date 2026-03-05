import cadquery as cq
import math

# Parameters
Dbig = 20.0
Rbig = Dbig/2
Dsmall = 10.0
Rsmall = Dsmall/2
barWidth = 12.0
L = 60.0
slotLength = 30.0
slotWidth = 4.0
Dhole_big = 10.0
Rhole_big = Dhole_big/2
Dhole_small = 6.0
Rhole_small = Dhole_small/2

# Derived
Zcenter_small = -Dbig/2 + Rsmall
slotCenterX = L/2
slotCenterZ = Zcenter_small/2
angle = math.degrees(math.atan2(Zcenter_small, L))

# Bar
bar = (
    cq.Workplane("XZ")
    .transformed(offset=(0, -barWidth/2, 0))
    .polyline([
        (0, -Dbig/2),
        (0,  Dbig/2),
        (L, -Dbig/2 + Dsmall),
        (L, -Dbig/2),
    ])
    .close()
    .extrude(barWidth)
)

# Big and small cylinders
bigCyl = (
    cq.Workplane("XZ")
    .transformed(offset=(0, -barWidth/2, 0))
    .circle(Rbig)
    .extrude(barWidth)
)
smallCyl = (
    cq.Workplane("XZ")
    .transformed(offset=(L, -barWidth/2, Zcenter_small))
    .circle(Rsmall)
    .extrude(barWidth)
)

# Holes
holeBig = (
    cq.Workplane("XZ")
    .transformed(offset=(0, -barWidth/2, 0))
    .circle(Rhole_big)
    .extrude(barWidth)
)
holeSmall = (
    cq.Workplane("XZ")
    .transformed(offset=(L, -barWidth/2, Zcenter_small))
    .circle(Rhole_small)
    .extrude(barWidth)
)

# Slot cutter
slotCutter = (
    cq.Workplane("XZ")
    .transformed(offset=(slotCenterX, -barWidth/2, slotCenterZ), rotate=(0, angle, 0))
    .rect(slotLength, slotWidth)
    .extrude(barWidth * 2)
)

# Assemble
result = (
    bar
    .union(bigCyl)
    .union(smallCyl)
    .cut(holeBig)
    .cut(holeSmall)
    .cut(slotCutter)
)