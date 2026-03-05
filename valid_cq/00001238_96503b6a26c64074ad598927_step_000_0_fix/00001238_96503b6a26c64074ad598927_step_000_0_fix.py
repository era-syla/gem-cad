import cadquery as cq

# Parameters
base_d = 100
base_h = 5
boss_d = 60
boss_h = 8
notch_w = 10
notch_d = base_h
hole_d = 15
hole_r = 20
square_w = 8
square_r = 20
slot_w = 5
slot_l = boss_d * 1.1

# Base disk
result = cq.Workplane("XY").circle(base_d/2).extrude(base_h)

# Cut notches in outer base
for angle in [0, 180]:
    notch = (
        cq.Workplane("XY")
        .workplane(offset=base_h)
        .transformed(rotate=(0, 0, angle))
        .center(base_d/2, 0)
        .rect(notch_w, notch_w)
        .extrude(-notch_d)
    )
    result = result.cut(notch)

# Boss on top of base
boss = (
    cq.Workplane("XY")
    .workplane(offset=base_h)
    .circle(boss_d/2)
    .extrude(boss_h)
)
result = result.union(boss)

# Slot through boss
slot = (
    cq.Workplane("XY")
    .workplane(offset=base_h)
    .rect(slot_w, slot_l)
    .extrude(boss_h)
)
result = result.cut(slot)

# Circular holes in boss
for angle in [0, 180]:
    hole = (
        cq.Workplane("XY")
        .workplane(offset=base_h)
        .transformed(rotate=(0, 0, angle))
        .center(hole_r, 0)
        .circle(hole_d/2)
        .extrude(boss_h)
    )
    result = result.cut(hole)

# Square holes in boss
for y in [square_r, -square_r]:
    sq = (
        cq.Workplane("XY")
        .workplane(offset=base_h)
        .center(0, y)
        .rect(square_w, square_w)
        .extrude(boss_h)
    )
    result = result.cut(sq)