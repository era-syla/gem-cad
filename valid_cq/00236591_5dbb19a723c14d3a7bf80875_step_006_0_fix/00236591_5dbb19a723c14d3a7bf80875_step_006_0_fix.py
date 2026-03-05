import cadquery as cq

outer_d = 70
inner_d = 60
height = 8
rim_height = 2
rim_inner_offset = 1
groove_depth = 1
groove_width = 0.5
slot_width = 6
slot_height = 2
text_str = "SAMSUNG LVPS"
text_height = 1
text_depth = 0.3

result = (
    cq.Workplane("XY")
    .circle(outer_d/2)
    .circle(inner_d/2)
    .extrude(height)
    .faces(">Z")
    .workplane()
    .circle(outer_d/2)
    .circle(inner_d/2 + rim_inner_offset)
    .extrude(rim_height)
)

for r in [outer_d/2 - 1, outer_d/2 - 2]:
    result = (
        result.faces(">Z")
        .workplane()
        .circle(r)
        .circle(r - groove_width)
        .cutBlind(groove_depth)
    )

for angle in (0, 180):
    result = (
        result.faces(">Z")
        .workplane()
        .transformed(rotate=(0, 0, angle))
        .moveTo((inner_d/2 + rim_inner_offset + outer_d/2)/2, 0)
        .rect(slot_width, slot_height)
        .cutBlind(rim_height)
    )

result = (
    result.faces(">Z")
    .workplane(offset=rim_height*0.5)
    .transformed(rotate=(90, 0, 0))
    .text(text_str, text_height, text_depth)
)