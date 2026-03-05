import cadquery as cq

# Parameters
L1 = 20      # length of left flat section
L2 = 30      # length of arch section (equal to 2*R)
L3 = 15      # length of right section
W  = 20      # block width in Y
T  = 5       # base plate thickness
R  = 15      # arch radius
Tw = 5       # side wall thickness
Hs = T + R   # full height of arch and side walls

# Build left flat plate
plate_left = cq.Workplane("XY").box(L1, W, T, centered=(False, True, False))

# Build middle base plate
plate_mid = cq.Workplane("XY").box(L2, W, T, centered=(False, True, False)).translate((L1, 0, 0))

# Build right base plate
plate_right_base = cq.Workplane("XY").box(L3, W, T, centered=(False, True, False)).translate((L1 + L2, 0, 0))

# Build right side walls
side1 = (
    cq.Workplane("XY")
    .box(L3, Tw, Hs, centered=(False, True, False))
    .translate((L1 + L2,  W/2 - Tw/2, 0))
)
side2 = (
    cq.Workplane("XY")
    .box(L3, Tw, Hs, centered=(False, True, False))
    .translate((L1 + L2, -W/2 + Tw/2, 0))
)

# Union base and side walls
base = plate_left.union(plate_mid).union(plate_right_base).union(side1).union(side2)

# Build half-cylinder arch on top of middle section
# Create full cylinder extruded along X
cyl_full = (
    cq.Workplane(cq.Plane(cq.Vector(L1, 0, T), cq.Vector(1, 0, 0)))
    .circle(R)
    .extrude(L2, combine=False)
)
# Cut away the bottom half of the cylinder (z < T)
cutter = (
    cq.Workplane("XY", origin=(L1 + L2/2, 0, 0))
    .box(L2 + 10, W + 10, T, centered=(True, True, False))
)
cyl_half = cyl_full.cut(cutter)

# Combine base and arch
pre_holes = base.union(cyl_half)

# Drill holes on left flat plate
x1 = L1/3
x2 = 2*L1/3
hole_dia = 5
depth = Hs + 2
result = (
    pre_holes
    .faces(">Z").workplane(offset=0)
    .pushPoints([(x1, 0), (x2, 0)])
    .hole(hole_dia, depth)
    # Drill hole on top of arch
    .faces(">Z").workplane(offset=0)
    .pushPoints([(L1 + L2/2, 0)])
    .hole(hole_dia, depth)
)
