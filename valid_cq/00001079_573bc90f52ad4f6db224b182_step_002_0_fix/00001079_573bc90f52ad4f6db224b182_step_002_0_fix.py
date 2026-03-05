import cadquery as cq

# Parameters
base_th = 5
boss_d = 20
boss_h = 15
hub_d = 25
tube_od = 15
tube_id = 10
tube_h = 80
hole_d = 6
slot_w = 3

# Positions for horizontal bosses
pos1 = (30, 0)
pos2 = (-15, -26)

# Base plate as triangular prism
result = (
    cq.Workplane("XY")
    .polyline([(0, 0), pos1, pos2])
    .close()
    .extrude(base_th)
)

# Add horizontal clamp bosses
for pos in (pos1, pos2):
    result = result.union(
        cq.Workplane("XY")
        .center(*pos)
        .circle(boss_d / 2)
        .extrude(boss_h)
    )

# Add central hub
result = result.union(
    cq.Workplane("XY")
    .circle(hub_d / 2)
    .extrude(boss_h)
)

# Add vertical tube
result = result.union(
    cq.Workplane("XY")
    .workplane(offset=boss_h)
    .circle(tube_od / 2)
    .extrude(tube_h)
)

# Bore the vertical tube
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=boss_h)
    .circle(tube_id / 2)
    .extrude(tube_h + 1)
)

# Drill holes in horizontal bosses
result = (
    result.faces(">Z")
    .workplane()
    .center(*pos1)
    .circle(hole_d / 2)
    .cutBlind(-boss_h)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(*pos2)
    .circle(hole_d / 2)
    .cutBlind(-boss_h)
)

# Cut slot in one horizontal boss
slot_len = boss_h + 2
result = (
    result.faces(">Z")
    .workplane()
    .center(*pos2)
    .rect(slot_w, slot_len)
    .cutBlind(-boss_h)
)