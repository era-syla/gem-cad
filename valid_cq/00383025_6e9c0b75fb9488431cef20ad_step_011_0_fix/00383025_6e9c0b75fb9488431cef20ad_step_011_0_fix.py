import cadquery as cq
import math

# Build the basic plate by union of a central disk and six outer lobes
base = cq.Workplane("XY").circle(30).extrude(5)
solids = [base]
for i in range(6):
    angle = math.radians(360.0/6 * i)
    x = 30 * math.cos(angle)
    y = 30 * math.sin(angle)
    solids.append(
        cq.Workplane("XY")
        .transformed(offset=(x, y, 0))
        .circle(10)
        .extrude(5)
    )
result = solids[0]
for s in solids[1:]:
    result = result.union(s)

# Fillet the vertical edges for a rounded profile
result = result.edges("|Z").fillet(2)

# Prepare hole patterns
points_big = []
# Mid‐arm holes at radius 30
for i in range(6):
    angle = math.radians(360.0/6 * i)
    points_big.append((30 * math.cos(angle), 30 * math.sin(angle)))
# End‐arm holes at radius 40
for i in range(6):
    angle = math.radians(360.0/6 * i)
    points_big.append((40 * math.cos(angle), 40 * math.sin(angle)))

points_small = []
# Central small holes: 4 at radius 10, 4 at radius 20
for r in (10, 20):
    for i in range(4):
        angle = math.radians(360.0/4 * i)
        points_small.append((r * math.cos(angle), r * math.sin(angle)))

# Drill the holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(points_big)
    .hole(3, 5)
    .pushPoints(points_small)
    .hole(2, 5)
)

# 'result' now holds the final solid geometry
