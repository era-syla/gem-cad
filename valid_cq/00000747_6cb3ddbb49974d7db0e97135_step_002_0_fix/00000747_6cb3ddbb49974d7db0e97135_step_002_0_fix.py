import cadquery as cq
import math

# Parameters
len_big = 20
d_big = 15
bore_d = 8
bore_depth = 10
hex_d = 6
hex_depth = 5
flange_t = 3
flange_d = 25
gear_hub_d = 10
gear_len = 15
num_teeth = 12
tooth_thick = 3
tooth_depth = 2
len_small = 50
d_small = 8

# Build base shaft, flange, gear hub, and small shaft
result = (
    cq.Workplane("XY")
    .cylinder(len_big, d_big)
    .faces("<Z").workplane().circle(bore_d/2).cutBlind(bore_depth)
    .faces("<Z").workplane().polygon(6, hex_d).cutBlind(hex_depth)
    .workplane(offset=len_big).cylinder(flange_t, flange_d)
    .workplane(offset=len_big + flange_t).cylinder(gear_len, gear_hub_d)
    .workplane(offset=len_big + flange_t + gear_len).cylinder(len_small, d_small)
)

# Add straight gear teeth around the gear hub
for i in range(num_teeth):
    angle = 360.0 / num_teeth * i
    tooth = (
        cq.Workplane("YZ")
        .transformed(offset=(gear_hub_d/2, 0, len_big + flange_t))
        .rect(tooth_thick, gear_len)
        .extrude(tooth_depth)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(tooth)

# result contains the final solid
result