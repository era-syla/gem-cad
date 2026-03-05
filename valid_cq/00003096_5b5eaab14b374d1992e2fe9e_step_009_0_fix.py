import cadquery as cq

# Nylon insert lock nut (nylock nut)
# Parameters
hex_width = 13.0      # across flats
hex_height = 6.0      # height of hex portion
nylon_height = 4.0    # height of nylon insert portion
total_height = hex_height + nylon_height
hole_r = 4.5          # thread hole radius (M8 ~ 4mm radius)
nylon_r = 5.5         # nylon insert inner radius
outer_r = 7.5         # outer radius of round nylon portion
chamfer_size = 1.2

# Build hex body
hex_body = (
    cq.Workplane("XY")
    .polygon(6, hex_width / 0.866 * 0.866 * 2 / 2)  # across-flats to circumradius
    .extrude(hex_height)
)

# Actually, use polygon with diameter = across-corners
# across flats = hex_width, across corners = hex_width / cos(30) 
af = hex_width  # across flats
ac = af / 0.866  # across corners (diameter)

hex_body = (
    cq.Workplane("XY")
    .polygon(6, ac)
    .extrude(hex_height)
)

# Add chamfers on top and bottom edges of hex
hex_body = (
    hex_body
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

hex_body = (
    hex_body
    .faces("<Z")
    .edges()
    .chamfer(chamfer_size)
)

# Build nylon insert cap (cylindrical portion on top)
nylon_cap = (
    cq.Workplane("XY")
    .workplane(offset=hex_height)
    .circle(outer_r)
    .extrude(nylon_height)
)

# Chamfer top edge of nylon cap
nylon_cap = (
    nylon_cap
    .faces(">Z")
    .edges()
    .chamfer(1.0)
)

# Combine hex body and nylon cap
combined = hex_body.union(nylon_cap)

# Cut through-hole (threaded hole simulation)
combined = (
    combined
    .faces("<Z")
    .workplane()
    .circle(hole_r)
    .cutThruAll()
)

# Add nylon insert ring groove (recessed ring inside nylon portion)
# Create a smaller inner bore in the nylon portion
nylon_bore = (
    cq.Workplane("XY")
    .workplane(offset=hex_height)
    .circle(nylon_r)
    .extrude(nylon_height - 1.5)
)

combined = combined.cut(nylon_bore)

# Add inner chamfer/fillet on the nylon bore entry
# Add a groove ring detail
groove = (
    cq.Workplane("XY")
    .workplane(offset=hex_height + 0.5)
    .circle(nylon_r + 0.3)
    .circle(nylon_r - 0.3)
    .extrude(0.6)
)

# Add fillet to top face of hex where it meets the nylon cap
result = combined