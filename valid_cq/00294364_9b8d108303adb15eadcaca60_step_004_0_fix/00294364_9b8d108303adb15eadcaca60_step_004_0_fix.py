import cadquery as cq

rod_length = 150
rod_radius = 5
collar_length = 10
collar_radius = 6
knob_length = 3
knob_radius = 8

result = (
    cq.Workplane("XY")
    .circle(rod_radius)
    .extrude(rod_length)
    .faces(">Z")
    .workplane()
    .circle(collar_radius)
    .extrude(collar_length)
    .faces(">Z")
    .workplane()
    .circle(knob_radius)
    .extrude(knob_length)
)