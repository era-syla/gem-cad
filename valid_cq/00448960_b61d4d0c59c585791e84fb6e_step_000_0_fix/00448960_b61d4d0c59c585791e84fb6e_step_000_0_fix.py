import cadquery as cq

thickness = 4
R_left = 10
R_right = 7
R_inner = 3
bar_half = 3
center_dist = 60

bar_len = center_dist - R_left - R_right
slot_len = R_right + R_inner
slot_center = center_dist + (R_right - R_inner) / 2

left = cq.Workplane("XY").circle(R_left).extrude(thickness)
bar = (
    cq.Workplane("XY")
    .rect(bar_len, 2 * bar_half)
    .extrude(thickness)
    .translate((R_left + bar_len / 2, 0, 0))
)
outer = (
    cq.Workplane("XY")
    .circle(R_right)
    .extrude(thickness)
    .translate((center_dist, 0, 0))
)

result = left.union(bar).union(outer)

hole = (
    cq.Workplane("XY")
    .circle(R_inner)
    .extrude(thickness)
    .translate((center_dist, 0, 0))
)
result = result.cut(hole)

slot = (
    cq.Workplane("XY")
    .rect(slot_len, 2 * bar_half)
    .extrude(thickness)
    .translate((slot_center, 0, 0))
)
result = result.cut(slot)