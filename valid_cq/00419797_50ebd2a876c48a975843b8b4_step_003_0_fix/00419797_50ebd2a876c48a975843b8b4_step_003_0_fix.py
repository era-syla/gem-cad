import cadquery as cq

# Parameters
length = 150.0
halfHeight = 10.0
lipThickness = 1.5
slotDepth = 3.0
headHalf = 5.0
neckHalf = 3.0

# 2D cross-section profile
pts = [
    (-headHalf,  halfHeight),
    ( headHalf,  halfHeight),
    ( headHalf,  halfHeight - lipThickness),
    ( neckHalf,  halfHeight - lipThickness),
    ( neckHalf,  halfHeight - lipThickness - slotDepth),
    ( headHalf,  halfHeight - lipThickness - slotDepth),
    ( headHalf, -halfHeight + lipThickness + slotDepth),
    ( neckHalf, -halfHeight + lipThickness + slotDepth),
    ( neckHalf, -halfHeight + lipThickness),
    ( headHalf, -halfHeight + lipThickness),
    ( headHalf, -halfHeight),
    (-headHalf, -halfHeight),
    (-headHalf, -halfHeight + lipThickness),
    (-neckHalf, -halfHeight + lipThickness),
    (-neckHalf, -halfHeight + lipThickness + slotDepth),
    (-headHalf, -halfHeight + lipThickness + slotDepth),
    (-headHalf,  halfHeight - lipThickness - slotDepth),
    (-neckHalf,  halfHeight - lipThickness - slotDepth),
    (-neckHalf,  halfHeight - lipThickness),
    (-headHalf,  halfHeight - lipThickness),
]

# Build the extrusion
result = (
    cq.Workplane("XY")
      .polyline(pts)
      .close()
      .extrude(length)
)

# Drill a hole through one narrow face
# Hole diameter
hole_dia = 4.0
# Position the hole at X = +headHalf, Y = 0, Z = length/2
hole = (
    cq.Workplane("YZ", origin=(headHalf, 0, length / 2.0))
      .circle(hole_dia / 2.0)
      .extrude(- (2 * headHalf + 1.0))  # extrude into the part
)

result = result.cut(hole)