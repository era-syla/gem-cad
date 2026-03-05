import cadquery as cq

# Parameters
length = 120
width = 20
thickness = 10
halfCylLen = 20
halfCylRad = width/2
holeDiam = 4
pocketDiam = width
pocketDepth = 5

# Base block
base = cq.Workplane("XY").box(length, width, thickness)

# Half cylinder on left end
halfCyl = (
    cq.Workplane("YZ", origin=(0, 0, thickness))
    .circle(halfCylRad)
    .extrude(halfCylLen)
)
# Cut away the bottom half of that cylinder so only the top half remains
cutBox = cq.Workplane("XY").box(length*2, width*2, thickness, centered=(True, True, False))
halfCyl = halfCyl.cut(cutBox)

# Combine base and half cylinder
result = base.union(halfCyl)

# Drill small vertical holes (through) at specified XY positions
holeDepth = thickness + halfCylRad
holePoints = [(10, 0), (60, 0), (90, 0)]
for x, y in holePoints:
    result = result.cut(
        cq.Workplane("XY", origin=(x, y, thickness + halfCylRad))
        .circle(holeDiam/2)
        .extrude(-holeDepth)
    )

# Add a circular pocket on the right end
pocketX = length - halfCylLen/2
result = result.cut(
    cq.Workplane("XY", origin=(pocketX, 0, thickness))
    .circle(pocketDiam/2)
    .extrude(-pocketDepth)
)