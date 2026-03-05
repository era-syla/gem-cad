import cadquery as cq

# Parameters
L_long = 110.0
L_short = 35.0
W = 14.0
H = 20.0
wall = 1.5
taper_L = 30.0
taper_H = 6.0
boss_dia = 7.0
boss_hole = 3.0
boss_h = 5.0
boss_x = 60.0
boss_z = H / 2
fillet_r_out = 6.0
fillet_r_in = 2.0

# 1. Base Sketch & Extrude
pts = [
    (0, 0),
    (L_long, 0),
    (L_long, W),
    (W, W),
    (W, L_short),
    (0, L_short)
]

base = cq.Workplane("XY").polyline(pts).close().extrude(H)

# 2. Vertical Fillets
base = base.edges("|Z").edges(cq.NearestToPointSelector((0, 0, H/2))).fillet(fillet_r_out)
base = base.edges("|Z").edges(cq.NearestToPointSelector((W, W, H/2))).fillet(fillet_r_in)
base = base.edges("|Z").edges(cq.NearestToPointSelector((L_long, 0, H/2))).fillet(fillet_r_in)
base = base.edges("|Z").edges(cq.NearestToPointSelector((L_long, W, H/2))).fillet(fillet_r_in)
base = base.edges("|Z").edges(cq.NearestToPointSelector((0, L_short, H/2))).fillet(fillet_r_in)
base = base.edges("|Z").edges(cq.NearestToPointSelector((W, L_short, H/2))).fillet(fillet_r_in)

# 3. Taper Cut at the far end of the long arm
taper = cq.Workplane("XZ").moveTo(L_long, 0) \
    .lineTo(L_long - taper_L, 0) \
    .lineTo(L_long, taper_H) \
    .close().extrude(W * 2)
base = base.cut(taper)

# 4. Shell the body from the top
part = base.faces(">Z").shell(-wall)

# 5. Add Side Boss
boss = cq.Workplane("XZ").center(boss_x, boss_z).circle(boss_dia / 2).extrude(-boss_h)
part = part.union(boss)

# 6. Boss Hole
hole1 = cq.Workplane("XZ").workplane(offset=-boss_h - 1) \
    .center(boss_x, boss_z).circle(boss_hole / 2).extrude(boss_h + wall + 5)
part = part.cut(hole1)

# 7. Short Arm Mounting Hole
hole2 = cq.Workplane("YZ").workplane(offset=-2) \
    .center(L_short - 6, 6).circle(1.5).extrude(W + 5)
part = part.cut(hole2)

# 8. Create Mirrored Pair to match the image
part_right = part.translate((20, 20, 0))
part_left = part.mirror("XZ").translate((-20, -20, 0))

result = part_right.union(part_left)