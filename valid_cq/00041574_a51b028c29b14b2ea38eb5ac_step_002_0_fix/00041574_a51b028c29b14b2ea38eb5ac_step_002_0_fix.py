import cadquery as cq

plate_length = 100
plate_width = 70
plate_thickness = 3
fillet_radius = 5
slot_half_width = 20
slot_depth = 40
cut_depth = 2

result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .faces(">Z").workplane()
    .polyline([
        (-slot_half_width,  slot_half_width),
        ( slot_half_width,  slot_half_width),
        ( slot_half_width,  slot_half_width - slot_depth)
    ])
    .threePointArc(
        (0, -slot_depth),
        (-slot_half_width, slot_half_width - slot_depth)
    )
    .close()
    .cutBlind(-cut_depth)
    .edges("|Z")
    .fillet(fillet_radius)
)