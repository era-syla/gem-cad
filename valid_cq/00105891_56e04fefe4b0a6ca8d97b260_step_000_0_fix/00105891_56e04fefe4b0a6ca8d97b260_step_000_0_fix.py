import cadquery as cq

# Parameters
R = 40             # Sphere radius
rneck = 15         # Neck radius
neck_h = 10        # Neck height
ring_r = 17        # Ring outer radius
ring_h = 2         # Ring height
ring_gap = 2       # Gap between rings
sheet_th = 2       # Sheet thickness
sheet_w = 100      # Sheet width
sheet_d = 50       # Sheet depth
handle_rad = 2     # Handle tube radius

# Body: hemisphere (sphere translated down so top is at z=0)
body = cq.Workplane("XY").sphere(R).translate((0, 0, -R))

# Neck cylinder
neck = cq.Workplane("XY").workplane(offset=0).circle(rneck).extrude(neck_h)

# Decorative rings on neck
ring1 = cq.Workplane("XY", origin=(0, 0, neck_h)).circle(ring_r).extrude(ring_h)
ring2 = cq.Workplane("XY", origin=(0, 0, neck_h + ring_h + ring_gap)).circle(ring_r).extrude(ring_h)

# Handle path in XZ plane, starting at neck, ending at body side
path = (
    cq.Workplane("XZ", origin=(0, 0, neck_h - 1))
    .moveTo(0, 0)
    .spline([(15, 9), (18, 12), (25, 0), (28, -10)])
    .wire()
    .val()
)

# Sweep a small circle along the handle path
handle = (
    cq.Workplane("XY", origin=(0, 0, neck_h - 1))
    .circle(handle_rad)
    .sweep(path)
)

# Sheet plate above the neck
sheet_z = neck_h + 5
plate = (
    cq.Workplane("XY", origin=(0, 0, sheet_z + sheet_th / 2))
    .rect(sheet_w, sheet_d)
    .extrude(-sheet_th)
)

# Depression on the plate: a hexagon pocket
depression = (
    cq.Workplane("XY", origin=(0, 0, sheet_z))
    .polygon(6, 20)
    .extrude(-1)
)

# Assemble all parts
result = (
    body
    .union(neck)
    .union(ring1)
    .union(ring2)
    .union(handle)
    .union(plate)
    .cut(depression)
)