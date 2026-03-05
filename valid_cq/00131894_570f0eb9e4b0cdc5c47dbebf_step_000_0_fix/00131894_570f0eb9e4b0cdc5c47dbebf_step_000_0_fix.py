import cadquery as cq

# Parameters
body_radius = 10
body_length = 80
boss_outer = 12
boss_thickness = 5
rod_radius = 6
rod_length = 40
plate_thickness = 3
plate_spacing = 10
plate_width = 15  # along Y
plate_height = 20  # along Z
pin_radius = 2.5
pin_length = plate_thickness + plate_spacing + 2 * plate_thickness

# Main cylinder body
body = cq.Workplane("XY").circle(body_radius).extrude(body_length)

# Boss ring at mid
ring = (
    cq.Workplane("XY")
    .workplane(offset=body_length/2 - boss_thickness/2)
    .circle(boss_outer)
    .extrude(boss_thickness)
    .faces(">Z")
    .workplane()
    .circle(body_radius)
    .cutBlind(-boss_thickness)
)

# Rod
rod = cq.Workplane("XY").workplane(offset=body_length).circle(rod_radius).extrude(rod_length)

# Front clevis plates
plate_offset_z = body_length + rod_length
half_gap = plate_spacing/2 + plate_thickness/2
plates = []
# Plate on +X side
plates.append(
    cq.Workplane("YZ")
    .transformed(offset=(half_gap, 0, plate_offset_z))
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .faces(">X")
    .workplane()
    .hole(pin_radius*2)
)
# Plate on -X side
plates.append(
    cq.Workplane("YZ")
    .transformed(offset=(-half_gap-plate_thickness, 0, plate_offset_z))
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .faces(">X")
    .workplane()
    .hole(pin_radius*2)
)

# Pin
pin = (
    cq.Workplane("YZ")
    .transformed(offset=(-half_gap - plate_thickness - 1, 0, plate_offset_z + plate_height/2))
    .circle(pin_radius)
    .extrude(pin_length)
)

# Combine all parts
result = body.union(ring).union(rod).union(plates[0]).union(plates[1]).union(pin)