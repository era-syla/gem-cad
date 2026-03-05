import cadquery as cq

# Parameters
base_L = 80
base_W = 40
base_h = 4

rail_w = 6
rail_h = 2

pad_size = 18
pad_h = 2
pad_offset = 15

cyl_od = 12
cyl_h = 6
cyl_id = 6

slot_len = 10

# Build base
result = cq.Workplane("XY").box(base_L, base_W, base_h)

# Add bottom rails
rail_offset = (base_W - rail_w) / 2
result = (
    result
    .faces("<Z").workplane()
    .pushPoints([(0, rail_offset), (0, -rail_offset)])
    .box(base_L, rail_w, rail_h, centered=(True, True, False))
)

# Add top pads
pad_x = base_L/2 - pad_offset - pad_size/2
result = (
    result
    .faces(">Z").workplane()
    .pushPoints([(-pad_x, 0), (pad_x, 0)])
    .box(pad_size, pad_size, pad_h, centered=(True, True, False))
)

# Add cylindrical bosses
result = (
    result
    .faces(">Z").workplane()
    .pushPoints([(-pad_x, 0), (pad_x, 0)])
    .circle(cyl_od/2)
    .extrude(cyl_h)
)

# Drill through holes in the bosses
result = (
    result
    .faces(">Z").workplane()
    .pushPoints([(-pad_x, 0), (pad_x, 0)])
    .hole(cyl_id)
)

# Cut the end slot through between the rails
slot_w = base_W - 2*rail_w
slot = (
    cq.Workplane("XY")
    .transformed(offset=(base_L/2 - slot_len/2, 0, 0))
    .box(slot_len, slot_w, base_h)
)
result = result.cut(slot)