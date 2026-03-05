import cadquery as cq

head_dia = 10
shaft_dia = 6
shaft_length = 20
head_thickness = 4
rim_width = 1
rim_depth = 0.5
slot_depth = 2
slot_width = 1
cross_length = head_dia - 2 * rim_width

result = (
    cq.Workplane("XY")
    .circle(shaft_dia / 2)
    .extrude(shaft_length)
    .faces(">Z")
    .workplane()
    .circle(head_dia / 2)
    .extrude(head_thickness)
    .faces(">Z")
    .workplane()
    .circle((head_dia / 2) - rim_width)
    .cutBlind(-rim_depth)
    .rect(cross_length, slot_width)
    .cutBlind(-slot_depth)
    .rect(slot_width, cross_length)
    .cutBlind(-slot_depth)
)