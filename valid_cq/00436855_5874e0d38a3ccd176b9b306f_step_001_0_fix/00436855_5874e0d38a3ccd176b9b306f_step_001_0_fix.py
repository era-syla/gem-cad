import cadquery as cq

# Parameters
L = 60
W = 40
H = 10
tab_w = 20
tab_len = 8
boss_d = 20
boss_h = 4
inner_d = 8
inner_h = 2
corner_hole_d = 6
hole_offset_x = 10
hole_offset_y = 10
ch_depth = 2

# Base block
result = cq.Workplane("XY").box(L, W, H)

# Corner holes
hole_pts = [
    (-L/2 + hole_offset_x, -W/2 + hole_offset_y),
    (-L/2 + hole_offset_x,  W/2 - hole_offset_y),
    ( L/2 - hole_offset_x, -W/2 + hole_offset_y),
    ( L/2 - hole_offset_x,  W/2 - hole_offset_y),
]
result = result.faces(">Z").workplane().pushPoints(hole_pts).hole(corner_hole_d)

# Front and back tabs
t1 = cq.Workplane("XY").box(tab_w, tab_len, H).translate((L/2, -tab_len/2, H/2))
t2 = cq.Workplane("XY").box(tab_w, tab_len, H).translate((L/2, W + tab_len/2, H/2))
result = result.union(t1).union(t2)

# Bosses and inner cylinders
boss_positions = [(-15, 0), (15, 0)]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(boss_positions)
    .circle(boss_d / 2)
    .extrude(boss_h)
    .pushPoints(boss_positions)
    .circle(inner_d / 2)
    .extrude(inner_h)
)

# Channel cut
cuts = (
    cq.Workplane("XY")
    .workplane(offset=H)
    .pushPoints([(-15, 0)])
    .circle(boss_d / 2 + 2)
    .pushPoints([(15, 0)])
    .circle(boss_d / 2 + 2)
    .pushPoints([(0, 0)])
    .circle(3)
    .extrude(-ch_depth)
)
result = result.cut(cuts)