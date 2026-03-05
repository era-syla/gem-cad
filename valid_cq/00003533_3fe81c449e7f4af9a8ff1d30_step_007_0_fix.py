import cadquery as cq

# Rod end / heim joint style part
# Components:
# 1. Hex base at bottom
# 2. Cylindrical shank above hex
# 3. Fork/clevis body (cylindrical)
# 4. Ring/eye at top with hole

# Dimensions
hex_width = 14  # hex across flats
hex_height = 6
shank_dia = 10
shank_height = 12
body_dia = 16
body_height = 14
ring_outer_dia = 22
ring_inner_dia = 8
ring_thickness = 8
ring_offset_x = 0
ring_offset_z = body_height + ring_outer_dia * 0.5

# Build hex base
hex_base = (
    cq.Workplane("XY")
    .polygon(6, hex_width * 2 / 3 * 2)
    .extrude(hex_height)
)

# Shank (cylinder on top of hex)
shank = (
    cq.Workplane("XY")
    .workplane(offset=hex_height)
    .circle(shank_dia / 2)
    .extrude(shank_height)
)

# Main body cylinder
body = (
    cq.Workplane("XY")
    .workplane(offset=hex_height + shank_height)
    .circle(body_dia / 2)
    .extrude(body_height)
)

# Ring/eye - torus-like flat ring
# The ring is tilted - sits at an angle on top of the body
# Create the ring as a flat disk with hole, tilted

ring_center_z = hex_height + shank_height + body_height

# Ring disk
ring = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .transformed(offset=cq.Vector(0, ring_center_z + ring_outer_dia * 0.0, 0))
    .circle(ring_outer_dia / 2)
    .extrude(ring_thickness)
)

# Actually let's build this more carefully
# The eye/ring is oriented in a vertical plane (XZ plane rotated)
# Let's create the ring in XY plane then rotate it

# Ring body - flat disk
ring_solid = (
    cq.Workplane("XY")
    .circle(ring_outer_dia / 2)
    .extrude(ring_thickness)
)

# Hole through ring
ring_with_hole = (
    ring_solid
    .faces(">Z")
    .workplane()
    .circle(ring_inner_dia / 2)
    .cutThruAll()
)

# Rotate ring to be in vertical plane (rotate 90 degrees around X axis)
ring_rotated = ring_with_hole.rotate((0, 0, 0), (1, 0, 0), 90)

# Move ring to top of body
ring_positioned = ring_rotated.translate((0, 0, ring_center_z + ring_outer_dia / 2))

# Combine all parts
result = (
    hex_base
    .union(shank)
    .union(body)
    .union(ring_positioned)
)

# Add a groove/chamfer on the ring outer edge for aesthetics
# Add fillet where body meets ring - approximate by adding a small connector sphere
# Add the groove on ring - create a torus-like groove

# Create groove on ring (equator groove)
groove_r = ring_outer_dia / 2
groove_solid = (
    cq.Workplane("XY")
    .circle(groove_r + 1)
    .extrude(2)
    .translate((0, 0, ring_center_z + ring_outer_dia / 2 - 1))
)

# Rotate groove to match ring orientation
groove_rotated = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .transformed(offset=cq.Vector(0, ring_center_z + ring_outer_dia / 2, 0))
    .circle(groove_r + 2)
    .circle(groove_r - 0.5)
    .extrude(2)
)

# Simpler approach - just union everything cleanly
result = (
    hex_base
    .union(shank)
    .union(body)
    .union(ring_positioned)
)