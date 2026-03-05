import cadquery as cq

# Parameters
shaft_length = 100
shaft_radius = 15
cap_thickness = 8
cap_radius = 18
lug_height = 10
lug_width = 12
lug_depth = 8
hole_dia = 5

result = (
    cq.Workplane("XY")
    # central shaft
    .cylinder(shaft_length, shaft_radius)
    # top cap
    .faces(">Z").workplane().cylinder(cap_thickness, cap_radius)
    # top lug
    .faces(">Z")
    .workplane()
    .transformed(offset=(0, cap_radius - lug_depth/2, 0))
    .rect(lug_width, lug_depth)
    .extrude(lug_height)
    # hole through top lug
    .faces(">Z")
    .workplane()
    .transformed(offset=(0, cap_radius - lug_depth/2, 0))
    .hole(hole_dia)
    # bottom cap
    .faces("<Z").workplane().cylinder(cap_thickness, cap_radius)
    # bottom lug
    .faces("<Z")
    .workplane()
    .transformed(offset=(0, cap_radius - lug_depth/2, 0))
    .rect(lug_width, lug_depth)
    .extrude(-lug_height)
    # hole through bottom lug
    .faces("<Z")
    .workplane()
    .transformed(offset=(0, cap_radius - lug_depth/2, 0))
    .hole(hole_dia)
)