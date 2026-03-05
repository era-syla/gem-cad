import cadquery as cq

# Main plate dimensions
plate_w = 120
plate_d = 80
plate_h = 15

# Bottom rail dimensions
rail_w = 100
rail_d = 80
rail_h = 8
rail_offset_z = -rail_h / 2

# Create main top plate
result = (
    cq.Workplane("XY")
    .box(plate_w, plate_d, plate_h)
)

# Add bottom rail (centered, slightly narrower)
rail = (
    cq.Workplane("XY")
    .box(rail_w, rail_d, rail_h)
    .translate((0, 0, -(plate_h / 2 + rail_h / 2)))
)

result = result.union(rail)

# Notch cut on top-right edge (front face notch)
notch_w = 16
notch_d = 8
notch_h = plate_h + 2

notch = (
    cq.Workplane("XY")
    .box(notch_w, notch_d, notch_h)
    .translate((plate_w / 2 - notch_w / 2, plate_d / 2 - notch_d / 2, 0))
)

result = result.cut(notch)

# Notch on bottom-left (front face)
notch2 = (
    cq.Workplane("XY")
    .box(notch_w, notch_d, notch_h)
    .translate((-plate_w / 2 + notch_w / 2, -plate_d / 2 + notch_d / 2, 0))
)

result = result.cut(notch2)

# Large counterbore holes (2x) - left side
hole_large_d = 12
hole_small_d = 6
hole_depth = plate_h

# Left large hole
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-35, -15)])
    .hole(hole_large_d, hole_depth)
)

# Right large hole
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(20, 15)])
    .hole(hole_large_d, hole_depth)
)

# Small holes (mounting holes at corners)
small_hole_d = 4
corner_inset_x = 45
corner_inset_y = 28

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-corner_inset_x, -corner_inset_y),
        (-corner_inset_x, corner_inset_y),
        (corner_inset_x, -corner_inset_y),
        (corner_inset_x, corner_inset_y),
    ])
    .hole(small_hole_d, plate_h)
)

# Additional small holes near large holes
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-25, -15), (30, 15)])
    .hole(small_hole_d, plate_h)
)

# Slot/groove cut on the bottom rail front face
slot_w = rail_w
slot_h = 4
slot_d = 4

slot = (
    cq.Workplane("XY")
    .box(slot_w, slot_d, slot_h)
    .translate((0, -(rail_d / 2 - slot_d / 2), -(plate_h / 2 + rail_h - slot_h / 2)))
)

result = result.cut(slot)