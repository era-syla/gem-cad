import cadquery as cq

# Parameters for standard 2020 aluminum extrusion profile
size = 20.0
length = 400.0
slot_opening = 6.0
slot_width = 11.0
slot_depth = 6.0
slot_lip = 1.8
center_hole_dia = 5.0

# Calculate offsets for slot features
open_offset = size / 2 - slot_depth / 2
inner_offset = size / 2 - slot_depth + slot_lip / 2

# Create the 2D profile using a Sketch
sk = cq.Sketch().rect(size, size)

# Subtract top and bottom slot openings
sk = sk.push([(0, open_offset), (0, -open_offset)]).rect(slot_opening, slot_depth, mode='s').reset()
# Subtract left and right slot openings
sk = sk.push([(open_offset, 0), (-open_offset, 0)]).rect(slot_depth, slot_opening, mode='s').reset()

# Subtract top and bottom inner T-slots
sk = sk.push([(0, inner_offset), (0, -inner_offset)]).rect(slot_width, slot_lip, mode='s').reset()
# Subtract left and right inner T-slots
sk = sk.push([(inner_offset, 0), (-inner_offset, 0)]).rect(slot_lip, slot_width, mode='s').reset()

# Subtract the center hole
sk = sk.circle(center_hole_dia / 2, mode='s').reset()

# Extrude the profile to create the linear rail/extrusion
result = cq.Workplane("XY").placeSketch(sk).extrude(length)

# Optional: center the extrusion on the origin
result = result.translate((0, 0, -length / 2))