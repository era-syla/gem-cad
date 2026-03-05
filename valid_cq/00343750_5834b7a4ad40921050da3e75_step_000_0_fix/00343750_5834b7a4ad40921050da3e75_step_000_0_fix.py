import cadquery as cq

# Parameters
se_len = 20
body_len = 50
be_len = 20
se_w = 8
body_w = 16
be_w = 32
thickness = 6
slot_len = 12
slot_w = 4
small_hole_dia = 5
big_hole_dia = 8
fillet_r = 2

# Build the main profile and extrude
pts = [
    (0, se_w/2),
    (se_len, se_w/2),
    (se_len+body_len, body_w/2),
    (se_len+body_len+be_len, be_w/2),
    (se_len+body_len+be_len, -be_w/2),
    (se_len+body_len, -body_w/2),
    (se_len, -se_w/2),
    (0, -se_w/2),
]
result = cq.Workplane("XY").polyline(pts).close().extrude(thickness)

# Fillet all vertical edges
result = result.edges("|Z").fillet(fillet_r)

# Cut the elongated slot at the big end
slot_center_x = se_len + body_len + be_len/2
result = (
    result
    .faces(">Z")
    .workplane()
    .transformed(offset=(slot_center_x, 0, 0))
    .rect(slot_len, slot_w)
    .cutThruAll()
)

# Drill the small and large pin holes
total_len = se_len + body_len + be_len
# small hole at small end
sm_x = se_len/2 - total_len/2
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(sm_x, 0)])
    .hole(small_hole_dia)
)
# big hole at big end
bg_x = slot_center_x - total_len/2
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(bg_x, 0)])
    .hole(big_hole_dia)
)