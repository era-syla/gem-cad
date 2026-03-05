import cadquery as cq

# Parameters
stub_length = 10
stub_dia = 12
main_length = 80
main_dia = 14
slot_depth = 2
slot_width = 3

result = (
    cq.Workplane("XY")
    # Bottom stub
    .circle(stub_dia / 2).extrude(stub_length)
    # Main cylinder
    .faces(">Z").workplane().circle(main_dia / 2).extrude(main_length)
    # Cross slot on top face
    .faces(">Z").workplane()
    .rect(slot_width, main_dia).cutBlind(slot_depth)
    .rect(main_dia, slot_width).cutBlind(slot_depth)
)

result