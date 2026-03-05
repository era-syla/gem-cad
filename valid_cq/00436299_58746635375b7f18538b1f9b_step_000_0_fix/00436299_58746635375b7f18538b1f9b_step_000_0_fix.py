import cadquery as cq

width = 50
depth = 15
height = 100
corner_radius = 5

# Slot on front face
slot1_width = 30
slot1_height = 4
slot1_depth = 3
slot1_bottom_offset = 5

# Small vertical cutout on front face
slot2_width = 3
slot2_height = 10
slot2_depth = 3
slot2_left_offset = 10
slot2_bottom_offset = 8

result = (
    cq.Workplane("XY")
    .box(width, depth, height)
    .edges().fillet(corner_radius)
    .faces(">Y").workplane()
    # main front slot
    .rect(slot1_width, slot1_height)
    .cutBlind(-slot1_depth)
    # small vertical cutout
    .center(
        -width/2 + slot2_left_offset + slot2_width/2,
        -height/2 + slot2_bottom_offset + slot2_height/2
    )
    .rect(slot2_width, slot2_height)
    .cutBlind(-slot2_depth)
)