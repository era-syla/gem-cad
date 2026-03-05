import cadquery as cq

# Main rectangular tray/box - open front
# Dimensions estimated from image
width = 80
height = 50
depth = 30
wall = 3

# Create the outer box
outer = cq.Workplane("XY").box(width, depth, height)

# Create inner cutout (open on front face - negative Y direction)
inner_w = width - 2 * wall
inner_d = depth - wall  # open on one side
inner_h = height - 2 * wall

# Hollow out the box leaving bottom and three walls (open front)
inner_cut = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, wall / 2, 0))
    .box(inner_w, inner_d + wall, inner_h)
)

tray = outer.cut(inner_cut)

# Add circular hole in the back wall
tray = (
    tray
    .faces(">Y")
    .workplane()
    .hole(20)
)

# Create the cylindrical knob/pulley on the back
# It's a cylinder with grooves sitting on the back face
knob_radius = 18
knob_height = depth + 10  # extends beyond the tray depth

knob = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, height / 2 + knob_radius * 0.0, 0))
    .circle(knob_radius)
    .extrude(knob_height / 2, both=True)
)

# Position the knob at the top-back of the tray
# The knob appears to be centered vertically and sits on top of the back wall
knob = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, height / 2, 0))
    .circle(knob_radius)
    .extrude(knob_height / 2, both=True)
)

# Actually let's build as separate body and union
# Knob centered at top of back, extending in Y direction
knob_body = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(0, 0, height / 2))
    .circle(knob_radius)
    .extrude(depth / 2 + 5, both=True)
)

# Add grooves to knob
groove_depth = 2
groove_width = 4

knob_with_grooves = knob_body
for z_offset in [-6, 0, 6]:
    groove_cut = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, 0, height / 2 + z_offset))
        .circle(knob_radius - groove_depth)
        .extrude(groove_width / 2, both=True)
    )
    # Cut groove by subtracting a torus-like shape
    # Use cylinder approach
    outer_cyl = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, 0, height / 2 + z_offset))
        .circle(knob_radius + 1)
        .extrude(groove_width / 2, both=True)
    )
    inner_cyl = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, 0, height / 2 + z_offset))
        .circle(knob_radius - groove_depth)
        .extrude(groove_width / 2, both=True)
    )
    ring = outer_cyl.cut(inner_cyl)
    knob_with_grooves = knob_with_grooves.cut(ring)

# Combine tray and knob
result = tray.union(knob_with_grooves)