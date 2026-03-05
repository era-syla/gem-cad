import cadquery as cq

# Parameters
plate_w = 120.0
plate_t = 6.0
plate_h = 50.0

cut_w = 12.0
cut_h = 30.0
cut_dist = 45.0

block_w = 50.0
block_h = 30.0
block_t = 25.0

pin_r = 3.0
pin_h = 10.0
pin_dist = 22.0

# 1. Create the main front plate
result = cq.Workplane("XY").box(plate_w, plate_t, plate_h)

# 2. Add the rectangular cutouts
result = (
    result.faces(">Y").workplane()
    .pushPoints([(cut_dist, 0), (-cut_dist, 0)])
    .rect(cut_w, cut_h)
    .cutThruAll()
)

# 3. Create the back block, flush with the top edge
z_offset = plate_h / 2.0 - block_h / 2.0
result = (
    result.faces("<Y").workplane()
    .center(0, z_offset)
    .rect(block_w, block_h)
    .extrude(block_t)
)

# 4. Create the cylindrical pins on top of the back block
pin_y_center = -plate_t / 2.0 - block_t / 2.0
pins = (
    cq.Workplane("XY").workplane(offset=plate_h / 2.0)
    .center(0, pin_y_center)
    .pushPoints([(pin_dist / 2.0, 0), (-pin_dist / 2.0, 0)])
    .circle(pin_r)
    .extrude(pin_h)
)

# Combine geometry
result = result.union(pins)