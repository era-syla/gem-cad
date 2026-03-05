import cadquery as cq

# Main large cylinder (right side)
large_cyl_r = 22
large_cyl_h = 30

# Small cylinder (left/front protruding)
small_cyl_r = 10
small_cyl_h = 20

# Build the main body
main_body = (
    cq.Workplane("YZ")
    .circle(large_cyl_r)
    .extrude(large_cyl_h)
)

# Add the smaller protruding cylinder on the left side
small_cyl = (
    cq.Workplane("YZ")
    .circle(small_cyl_r)
    .extrude(small_cyl_h + large_cyl_h)
)

# Combine
body = main_body.union(small_cyl)

# Cut slots on the large cylinder - two rectangular notches on the side
# Slot 1 - top area
slot_w = 8
slot_h = 10
slot_depth = 5

# Cut rectangular slots into the large cylinder
# Slot on top
slot1 = (
    cq.Workplane("XY")
    .workplane(offset=large_cyl_h - slot_h - 5)
    .center(0, large_cyl_r - slot_depth/2)
    .rect(slot_w, slot_depth)
    .extrude(slot_h)
)

# Slot on bottom (mirror)
slot2 = (
    cq.Workplane("XY")
    .workplane(offset=large_cyl_h - slot_h - 5)
    .center(0, -(large_cyl_r - slot_depth/2))
    .rect(slot_w, slot_depth)
    .extrude(slot_h)
)

body = body.cut(slot1).cut(slot2)

# Cut a flat on both sides of the small cylinder (D-shape or flats)
flat_cut_offset = small_cyl_r - 3
flat_cut1 = (
    cq.Workplane("XZ")
    .workplane(offset=flat_cut_offset)
    .rect(small_cyl_h + large_cyl_h + 10, small_cyl_r * 2 + 10)
    .extrude(20)
)
flat_cut2 = (
    cq.Workplane("XZ")
    .workplane(offset=-flat_cut_offset)
    .rect(small_cyl_h + large_cyl_h + 10, small_cyl_r * 2 + 10)
    .extrude(20)
    .translate((0, -20, 0))
)

body = body.cut(flat_cut1).cut(flat_cut2)

# Add a small through hole in the center of the small cylinder face
center_hole = (
    cq.Workplane("YZ")
    .circle(1.5)
    .extrude(small_cyl_h + large_cyl_h + 5)
)

body = body.cut(center_hole)

# Add chamfer to the front face edge of the small cylinder
# Select edges at the front face (x = small_cyl_h + large_cyl_h)
try:
    result = body.faces(">X").edges().chamfer(1.0)
except:
    result = body

# Also chamfer the back face
try:
    result = result.faces("<X").edges().chamfer(1.0)
except:
    pass

result = result