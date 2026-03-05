import cadquery as cq

outer_diameter = 20
inner_diameter = 18
length = 80
slot_width = 2
slot_length = 60
cutout_length = 15
cutout_width = 4

result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(length)
    .faces(">Z")
    .workplane()
    .circle(inner_diameter / 2)
    .cutBlind(-length)
    .faces(">Z")
    .workplane()
    .moveTo(0, (outer_diameter / 2) - slot_width / 2)
    .slot2D(slot_length, slot_width)
    .cutThruAll()
    .faces("<Z")
    .workplane()
    .moveTo(0, (inner_diameter / 2))
    .slot2D(cutout_length, cutout_width)
    .cutThruAll()
)