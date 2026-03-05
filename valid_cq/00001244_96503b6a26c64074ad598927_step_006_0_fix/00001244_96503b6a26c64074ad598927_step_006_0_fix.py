import cadquery as cq

# Dimensions (mm)
thk = 2.5
head_len = 10.0
neck_len = 5.0
blade_len = 60.0
half_head_w = 10.0
half_neck_w = 5.0
half_blade_w = 3.0

# 2D profile of the key outline
coords = [
    (0.0,  half_head_w),
    (head_len,  half_head_w),
    (head_len,  half_neck_w),
    (head_len + neck_len,  half_neck_w),
    (head_len + neck_len,  half_blade_w),
    (head_len + neck_len + blade_len,  half_blade_w),
    (head_len + neck_len + blade_len, -half_blade_w),
    (head_len + neck_len, -half_blade_w),
    (head_len + neck_len, -half_neck_w),
    (head_len, -half_neck_w),
    (head_len, -half_head_w),
    (0.0, -half_head_w),
]

# Create base solid by extruding the 2D profile
result = cq.Workplane("XY").polyline(coords).close().extrude(thk)

# Cut two rectangular notches in the head
notch_w = 3.0
notch_h = 4.0
notch_offset = half_head_w * 0.6
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(head_len / 2,  notch_offset), (head_len / 2, -notch_offset)])
    .rect(notch_w, notch_h)
    .cutThruAll()
)

# Cut slot along the top of the blade
slot_w = 1.2
slot_depth = 1.6
slot_start = head_len + neck_len
slot_end = slot_start + blade_len - 5.0  # leave 5mm at the tip
slot_len = slot_end - slot_start
slot_center = slot_start + slot_len / 2.0

result = (
    result
    .faces(">Z")
    .workplane()
    .center(slot_center, 0)
    .rect(slot_len, slot_w)
    .cutBlind(-slot_depth)
)