import cadquery as cq
import math

# Parameters
th = 8
R_hub = 12
R_l = 8
hole_r = 4
arm_width = 6
arm_length = 30
pin_r = 5

# Lobe positions (angles 90°, 210°, 330°)
R_offset = R_hub + R_l
pos1 = (0, R_offset)
pos2 = (R_offset * math.cos(math.radians(210)), R_offset * math.sin(math.radians(210)))
pos3 = (R_offset * math.cos(math.radians(330)), R_offset * math.sin(math.radians(330)))

# Build base hub and lobes
result = cq.Workplane("XY").circle(R_hub).extrude(th)
for p in (pos1, pos2, pos3):
    result = result.union(
        cq.Workplane("XY")
        .center(p[0], p[1])
        .circle(R_l)
        .extrude(th)
    )

# Subtract through-holes in each lobe
for p in (pos1, pos2, pos3):
    result = result.cut(
        cq.Workplane("XY")
        .center(p[0], p[1])
        .circle(hole_r)
        .extrude(th + 1)
    )

# Subtract central hub hole
result = result.cut(
    cq.Workplane("XY")
    .circle(hole_r + 1)
    .extrude(th + 1)
)

# Build connecting bar for the two bottom lobes
min_x = min(pos2[0], pos3[0])
max_x = max(pos2[0], pos3[0])
total_length = (max_x - min_x) + arm_length
center_x = min_x + total_length / 2
bar_y = pos2[1]
result = result.union(
    cq.Workplane("XY")
    .center(center_x, bar_y)
    .rect(total_length, arm_width)
    .extrude(th)
)

# Add hinge pin cylinder at end of bar
pin_x = max_x + arm_length
result = result.union(
    cq.Workplane("XY")
    .center(pin_x, bar_y)
    .circle(pin_r)
    .extrude(th)
)