import cadquery as cq

# Parameters
base_r = 6
base_h = 3
shaft_r = 1.5
shaft_h = 40
inner_r = 5
lobe_r = 2
lobe_center_r = 6
knob_thickness = 4
hole_r = 1.5
lobe_count = 8

# Create base and shaft
result = (
    cq.Workplane("XY")
    .circle(base_r)
    .extrude(base_h)
    .faces(">Z")
    .workplane()
    .circle(shaft_r)
    .extrude(shaft_h)
)

# Create knob at origin
knob = cq.Workplane("XY").circle(inner_r).extrude(knob_thickness)
for i in range(lobe_count):
    angle = i * 360.0 / lobe_count
    lobe = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle))
        .moveTo(lobe_center_r, 0)
        .circle(lobe_r)
        .extrude(knob_thickness)
    )
    knob = knob.union(lobe)

# Cut central hole in knob
knob = knob.faces(">Z").workplane().circle(hole_r).cutThruAll()

# Position knob on top of shaft and combine
knob = knob.translate((0, 0, base_h + shaft_h))
result = result.union(knob)