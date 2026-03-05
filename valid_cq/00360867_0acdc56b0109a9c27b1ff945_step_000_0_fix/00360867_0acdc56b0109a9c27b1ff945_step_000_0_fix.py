import cadquery as cq

# Parameters
blockL = 80
blockW = 20
blockH = 20
slotL = 60
slotH = 10
pinD = 10
pinExt = 2
leverLen = 60
leverProfH = 4
leverThick = 6
bossD = 14
nutD = 10
nutTh = 6
mountHoleD = 8

# Base block with central slot
base = (
    cq.Workplane("XZ")
    .box(blockL, blockW, blockH)
    .cut(
        cq.Workplane("XZ")
        .box(slotL, blockW, slotH)
        .translate((0, 0, - (blockH - slotH)/2))  # lower the slot box so it cuts from mid-height downward
    )
)

# Pivot pin through block (with a small extension on both sides)
pin = (
    cq.Workplane("XZ")
    .circle(pinD/2)
    .extrude(blockW + pinExt * 2)
)

# Mounting holes: one pair on top, one pair on each side
base = (
    base
    # Top holes
    .faces(">Z")
    .workplane()
    .pushPoints([(-20, 0), (20, 0)])
    .hole(mountHoleD)
    # Side holes on Y-positive face
    .faces(">Y")
    .workplane(centerOption="CenterOfBoundBox")
    .pushPoints([(-20, 5), (20, 5)])
    .hole(mountHoleD)
    # Side holes on Y-negative face
    .faces("<Y")
    .workplane(centerOption="CenterOfBoundBox")
    .pushPoints([(-20, 5), (20, 5)])
    .hole(mountHoleD)
)

# Lever handle profile in XZ, extruded along Y
lever = (
    cq.Workplane("XZ", origin=(0, blockW/2 + pinExt, 0))
    .polyline([
        (pinD/2 + 5,  leverProfH/2),
        (leverLen,    leverProfH/2),
        (leverLen+2,  0),
        (leverLen,   -leverProfH/2),
        (pinD/2 + 5, -leverProfH/2)
    ])
    .close()
    .extrude(leverThick)
)

# Boss around pivot under lever
boss = (
    cq.Workplane("XZ", origin=(0, blockW/2 + pinExt, 0))
    .circle(bossD/2)
    .extrude(leverThick)
)

# Nut (hexagon) at end of pin outside lever
nut = (
    cq.Workplane("XZ", origin=(0, blockW/2 + pinExt + leverThick, 0))
    .polygon(6, nutD)
    .extrude(nutTh)
)

# Combine all parts
result = base.union(pin).union(lever).union(boss).union(nut)