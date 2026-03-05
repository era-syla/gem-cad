import cadquery as cq

thickness = 3.0
R1 = 7.0       # left pad radius
R2 = 10.0      # right pad radius
Wmid = 4.0     # width of the narrow mid section
center_dist = 100.0
Lmid = center_dist - R1 - R2
hole_dia = 3.0

# left pad
left_pad = cq.Workplane("XY").circle(R1).extrude(thickness)

# middle bar
mid_bar = (
    cq.Workplane("XY")
    .transformed(offset=(R1 + Lmid/2, 0, 0))
    .rect(Lmid, Wmid)
    .extrude(thickness)
)

# right pad
right_pad = (
    cq.Workplane("XY")
    .transformed(offset=(center_dist, 0, 0))
    .circle(R2)
    .extrude(thickness)
)

# combine parts
result = left_pad.union(mid_bar).union(right_pad)

# drill holes: one in the left pad center, two in the right pad
hole_positions = [
    (0, 0),
    (center_dist,  R2/2),
    (center_dist, -R2/2),
]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_dia)
)