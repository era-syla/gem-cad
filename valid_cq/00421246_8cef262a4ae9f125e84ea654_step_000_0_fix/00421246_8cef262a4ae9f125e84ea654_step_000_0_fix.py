import cadquery as cq

# Parameters
smaller_d = 16
left_len = 30
mid_flange_d = 25
mid_flange_thk = 5
body_d = 18
body_len = 40
right_flange_d = 20
right_flange_thk = 3
bore_d = 10
slot_len = 12
slot_w = 4

# Build main geometry: left tube, mid flange, body tube, right flange
result = (
    cq.Workplane("XY")
    .circle(smaller_d/2).extrude(left_len)
    .circle(mid_flange_d/2).extrude(mid_flange_thk)
    .circle(body_d/2).extrude(body_len)
    .circle(right_flange_d/2).extrude(right_flange_thk)
)

# Internal bore through entire part
result = result.faces("<Z").workplane().circle(bore_d/2).cutThruAll()

# Slot cut on top of body section
slot_center_z = left_len + mid_flange_thk + body_len/2
slot_cut = (
    cq.Workplane("XY")
    .transformed(offset=(0, body_d/2 - slot_w/2, slot_center_z))
    .box(body_d*2, slot_w, slot_len)
)
result = result.cut(slot_cut)