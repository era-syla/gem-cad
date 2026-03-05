import cadquery as cq

# Parameters
length_f = 40
width = 12
th = 2
base_h = 3
wall_h = 12
boss_r = 6
hole_r = 3
slot_w = width - 2 * th
slot_l = 20
length_m = slot_l + 6
post_x = length_f / 2 - boss_r * 1.5
post_offset_y = slot_w / 2 + th / 2

# Female housing
female = (
    cq.Workplane("XY")
    .box(length_f, width, base_h)
    .faces(">Z").workplane()
    .rect(length_f, width)
    .rect(length_f - 2 * th, width - 2 * th)
    .extrude(wall_h - base_h)
    .faces(">Z").workplane()
    .center(length_f / 2 - boss_r, 0)
    .circle(boss_r)
    .extrude(base_h)
    .faces(">Z").workplane()
    .center(length_f / 2 - boss_r, 0)
    .circle(hole_r)
    .cutThruAll()
)

# Vertical posts around slot
post1 = (
    cq.Workplane("XY")
    .center(post_x, post_offset_y)
    .rect(th, slot_w)
    .extrude(wall_h - base_h)
)
post2 = (
    cq.Workplane("XY")
    .center(post_x, -post_offset_y)
    .rect(th, slot_w)
    .extrude(wall_h - base_h)
)
female = female.union(post1).union(post2)

# Male sliding tab
male = (
    cq.Workplane("XY")
    .box(length_m, slot_w, base_h)
    .translate((-(length_f / 2 + length_m / 2), 0, base_h / 2))
)
# Stop block on male tab
stop = (
    cq.Workplane("XY")
    .box(th, slot_w, base_h)
    .translate((-(length_f / 2 + length_m + th / 2), 0, base_h / 2))
)
male = male.union(stop)

# Combine parts
result = female.union(male)