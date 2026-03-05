import cadquery as cq

length = 100
width = 10
thickness = 2
groove_width = 1
groove_depth = 0.5
offset_y = (width / 2 - groove_width / 2)

result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .center(0, offset_y)
    .rect(length, groove_width)
    .cutBlind(groove_depth)
    .faces(">Z")
    .workplane()
    .center(0, -offset_y)
    .rect(length, groove_width)
    .cutBlind(groove_depth)
)