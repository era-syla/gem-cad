import cadquery as cq

# Parameters
bar_width = 20
bar_height = 10
horiz_length = 100
vert_length = 80
x_intersect = -20
slot_margin = 10
slot_width = 8
boss_length = 20
boss_width = 10
boss_height = 10
slot_depth = bar_height / 2

# Horizontal bar
h = cq.Workplane("XY")\
    .center(0, 0)\
    .rect(horiz_length, bar_width)\
    .extrude(bar_height)

# Horizontal slot on the right limb
slot1_left = x_intersect + slot_margin
slot1_right = horiz_length/2 - slot_margin
slot1_length = slot1_right - slot1_left
slot1_center = (slot1_left + slot1_right) / 2

h = (
    h.faces(">Z")
     .workplane()
     .center(slot1_center, 0)
     .rect(slot1_length, slot_width)
     .cutBlind(-slot_depth)
)

# Boss on horizontal bar, flush at the intersection plane
boss1_center_x = x_intersect + boss_length/2
h = (
    h.faces(">Z")
     .workplane()
     .center(boss1_center_x, 0)
     .rect(boss_length, boss_width)
     .extrude(boss_height)
)

# Vertical bar
v = cq.Workplane("XY")\
    .center(x_intersect, 0)\
    .rect(bar_width, vert_length)\
    .extrude(bar_height)

# Vertical slot on the far limb
slot2_bottom = slot_margin
slot2_top = vert_length/2 - slot_margin
slot2_length = slot2_top - slot2_bottom
slot2_center = (slot2_bottom + slot2_top) / 2

v = (
    v.faces(">Z")
     .workplane()
     .center(0, slot2_center)
     .rect(slot_width, slot2_length)
     .cutBlind(-slot_depth)
)

# Boss on vertical bar, flush at the intersection plane toward the viewer
boss2_center_y = -boss_length/2
v = (
    v.faces(">Z")
     .workplane()
     .center(0, boss2_center_y)
     .rect(boss_width, boss_length)
     .extrude(boss_height)
)

# Combine both parts
result = h.union(v)