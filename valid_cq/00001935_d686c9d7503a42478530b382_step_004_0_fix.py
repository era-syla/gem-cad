import cadquery as cq

# Main body dimensions
body_length = 80
body_width = 28
body_height = 8
corner_radius = 10

# Create the main oval/rounded rectangular body
main_body = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .rect(body_length - 2*corner_radius, body_width)
    .extrude(body_height)
)

# Add rounded ends using cylinders
left_cap = (
    cq.Workplane("XY")
    .moveTo(-(body_length/2 - corner_radius), 0)
    .circle(body_width/2)
    .extrude(body_height)
)

right_cap = (
    cq.Workplane("XY")
    .moveTo((body_length/2 - corner_radius), 0)
    .circle(body_width/2)
    .extrude(body_height)
)

main_body = main_body.union(left_cap).union(right_cap)

# Create the two oval cutouts (left and right slots)
slot_length = 28
slot_width = 14
slot_height = body_height + 2
slot_corner = 6
slot_offset = 16

# Left slot
left_slot_body = (
    cq.Workplane("XY")
    .moveTo(-slot_offset, 0)
    .rect(slot_length - 2*slot_corner, slot_width)
    .extrude(slot_height)
)
left_slot_left = (
    cq.Workplane("XY")
    .moveTo(-slot_offset - (slot_length/2 - slot_corner), 0)
    .circle(slot_width/2)
    .extrude(slot_height)
)
left_slot_right = (
    cq.Workplane("XY")
    .moveTo(-slot_offset + (slot_length/2 - slot_corner), 0)
    .circle(slot_width/2)
    .extrude(slot_height)
)
left_slot = left_slot_body.union(left_slot_left).union(left_slot_right)

# Right slot
right_slot_body = (
    cq.Workplane("XY")
    .moveTo(slot_offset, 0)
    .rect(slot_length - 2*slot_corner, slot_width)
    .extrude(slot_height)
)
right_slot_left = (
    cq.Workplane("XY")
    .moveTo(slot_offset - (slot_length/2 - slot_corner), 0)
    .circle(slot_width/2)
    .extrude(slot_height)
)
right_slot_right = (
    cq.Workplane("XY")
    .moveTo(slot_offset + (slot_length/2 - slot_corner), 0)
    .circle(slot_width/2)
    .extrude(slot_height)
)
right_slot = right_slot_body.union(right_slot_left).union(right_slot_right)

# Cut slots from main body
main_body = main_body.cut(left_slot).cut(right_slot)

# Add thin connector tabs on the long sides (middle)
tab_length = 12
tab_width = 4
tab_height = 4

left_tab = (
    cq.Workplane("XY")
    .moveTo(-(body_length/2 + tab_length/2), 0)
    .rect(tab_length, tab_width)
    .extrude(tab_height)
)

right_tab = (
    cq.Workplane("XY")
    .moveTo((body_length/2 + tab_length/2), 0)
    .rect(tab_length, tab_width)
    .extrude(tab_height)
)

main_body = main_body.union(left_tab).union(right_tab)

# Add a small wall/divider in the center between the two slots
divider = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .rect(3, slot_width - 2)
    .extrude(body_height)
)
main_body = main_body.union(divider)

# Add rim/wall around slots - create inner raised border
# The slots have a raised frame around them
# Create raised border by adding a thin rim on top
rim_height = 3
rim_thickness = 2.5

# Left rim outer
left_rim_outer = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .moveTo(-slot_offset, 0)
    .rect(slot_length - 2*slot_corner + rim_thickness*2, slot_width + rim_thickness*2)
    .extrude(rim_height)
)
left_rim_outer_l = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .moveTo(-slot_offset - (slot_length/2 - slot_corner), 0)
    .circle(slot_width/2 + rim_thickness)
    .extrude(rim_height)
)
left_rim_outer_r = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .moveTo(-slot_offset + (slot_length/2 - slot_corner), 0)
    .circle(slot_width/2 + rim_thickness)
    .extrude(rim_height)
)
left_rim = left_rim_outer.union(left_rim_outer_l).union(left_rim_outer_r)

# Cut the inner part of rim
left_rim = left_rim.cut(
    cq.Workplane("XY").workplane(offset=body_height-1)
    .moveTo(-slot_offset, 0)
    .rect(slot_length - 2*slot_corner, slot_width).extrude(rim_height+2)
    .union(
        cq.Workplane("XY").workplane(offset=body_height-1)
        .moveTo(-slot_offset-(slot_length/2-slot_corner),0).circle(slot_width/2).extrude(rim_height+2)
    ).union(
        cq.Workplane("XY").workplane(offset=body_height-1)
        .moveTo(-slot_offset+(slot_length/2-slot_corner),0).circle(slot_width/2).extrude(rim_height+2)
    )
)

main_body = main_body.union(left_rim)

# Right rim
right_rim_outer = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .moveTo(slot_offset, 0)
    .rect(slot_length - 2*slot_corner + rim_thickness*2, slot_width + rim_thickness*2)
    .extrude(rim_height)
)
right_rim_outer_l = (
    cq.Workplane("XY").workplane(offset=body_height)
    .moveTo(slot_offset-(slot_length/2-slot_corner),0).circle(slot_width/2+rim_thickness).extrude(rim_height)
)
right_rim_outer_r = (
    cq.Workplane("XY").workplane(offset=body_height)
    .moveTo(slot_offset+(slot_length/2-slot_corner),0).circle(slot_width/2+rim_thickness).extrude(rim_height)
)
right_rim = right_rim_outer.union(right_rim_outer_l).union(right_rim_outer_r)
right_rim = right_rim.cut(
    cq.Workplane("XY").workplane(offset=body_height-1)
    .moveTo(slot_offset,0).rect(slot_length-2*slot_corner,slot_width).extrude(rim_height+2)
    .union(cq.Workplane("XY").workplane(offset=body_height-1).moveTo(slot_offset-(slot_length/2-slot_corner),0).circle(slot_width/2).extrude(rim_height+2))
    .union(cq.Workplane("XY").workplane(offset=body_height-1).moveTo(slot_offset+(slot_length/2-slot_corner),0).circle(slot_width/2).extrude(rim_height+2))
)

main_body = main_body.union(right_rim)

result = main_body