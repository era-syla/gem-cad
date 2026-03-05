import cadquery as cq

plate_thickness = 3.0
plate_length = 240.0
plate_width = 60.0
tab_width = 40.0
tab_depth = 10.0
tab_offset_x = 60.0

slot_w = 60.0
slot_h = 20.0
slot_offset_x = 80.0
slot_offset_y = tab_depth + (plate_width - slot_h) / 2

hole_d = 3.0
hole_positions = [
    (10.0, tab_depth + 10.0),
    (10.0, tab_depth + plate_width - 10.0),
    (plate_length - 10.0, tab_depth + 10.0),
    (plate_length - 10.0, tab_depth + plate_width - 10.0),
    (tab_offset_x + 10.0, 5.0),
    (tab_offset_x + tab_width - 10.0, 5.0),
    (tab_offset_x + 10.0, tab_depth - 5.0),
    (tab_offset_x + tab_width - 10.0, tab_depth - 5.0),
]

# Base outline with tab
base = (
    cq.Workplane("XY")
    .polyline([
        (0, tab_depth),
        (tab_offset_x, tab_depth),
        (tab_offset_x, 0),
        (tab_offset_x + tab_width, 0),
        (tab_offset_x + tab_width, tab_depth),
        (plate_length, tab_depth),
        (plate_length, tab_depth + plate_width),
        (0, tab_depth + plate_width),
    ])
    .close()
    .extrude(plate_thickness)
)

# Rectangular slot
base = (
    base.faces(">Z")
    .workplane()
    .transformed(offset=(slot_offset_x + slot_w / 2, slot_offset_y + slot_h / 2))
    .rect(slot_w, slot_h)
    .cutThruAll()
)

# Mounting holes
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_d)
)

# Engraved text on top face
texts = [
    ("CAM1: 1048.561", (150.0, tab_depth + 46.0)),
    ("CAM2: 256.874", (150.0, tab_depth + 38.0)),
    ("THIS SIDE UP HAND", (150.0, tab_depth + 30.0)),
]
wp = base.faces(">Z").workplane(offset=0.1)
for t, pos in texts:
    wp = wp.pushPoints([pos]).text(t, 4.0, 0.5, combine=True)

result = wp