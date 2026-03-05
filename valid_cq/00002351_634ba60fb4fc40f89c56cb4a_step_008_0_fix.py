import cadquery as cq

# Main body dimensions
W = 60  # width (x)
H = 45  # height (z)
D = 45  # depth (y)
corner_r = 5

# Build main box body with rounded edges
body = (
    cq.Workplane("XY")
    .box(W, D, H)
)

# Fillet all edges
body = body.edges().fillet(corner_r)

# --- Front face features (lens, small button) ---
# Large lens ring on front face
lens_x = -8
lens_y = 0  # centered vertically roughly
lens_outer_r = 14
lens_inner_r = 11
lens_depth = 3

front_lens_ring = (
    cq.Workplane("YZ")
    .workplane(offset=W/2)
    .circle(lens_outer_r)
    .extrude(lens_depth)
)

# Lens inner (glass)
lens_glass = (
    cq.Workplane("YZ")
    .workplane(offset=W/2)
    .circle(lens_inner_r)
    .extrude(lens_depth + 1)
)

# Small button on front-top
small_btn = (
    cq.Workplane("YZ")
    .workplane(offset=W/2)
    .center(-8, 10)
    .circle(5)
    .extrude(2)
)

# --- Top face features ---
# Top button (dome/circle)
top_btn = (
    cq.Workplane("XY")
    .workplane(offset=H/2)
    .center(-12, -8)
    .circle(8)
    .extrude(3)
)

# Top small circle
top_small_circle = (
    cq.Workplane("XY")
    .workplane(offset=H/2)
    .center(8, -10)
    .circle(5)
    .extrude(2)
)

# Top LCD screen (rounded rect)
top_lcd = (
    cq.Workplane("XY")
    .workplane(offset=H/2)
    .center(15, 5)
    .rect(18, 14)
    .extrude(1.5)
)

# --- Side features ---
# Right side circle
right_circle = (
    cq.Workplane("XZ")
    .workplane(offset=D/2)
    .center(10, -5)
    .circle(5)
    .extrude(2)
)

# Left side - USB port slot
usb_port = (
    cq.Workplane("XZ")
    .workplane(offset=-D/2)
    .center(-15, -8)
    .rect(8, 4)
    .extrude(3)
)

# Left side small hole (top)
left_hole_top = (
    cq.Workplane("XZ")
    .workplane(offset=-D/2)
    .center(-15, 5)
    .circle(2)
    .extrude(3)
)

# Left side small hole (bottom)
left_hole_bot = (
    cq.Workplane("XZ")
    .workplane(offset=-D/2)
    .center(-15, -18)
    .circle(2)
    .extrude(3)
)

# Combine all additive features
result = (
    body
    .union(front_lens_ring)
    .union(small_btn)
    .union(top_btn)
    .union(top_small_circle)
    .union(top_lcd)
    .union(right_circle)
)

# Cut ports/holes
result = (
    result
    .cut(usb_port)
    .cut(left_hole_top)
    .cut(left_hole_bot)
)

# Add lens detail - cut inner lens
lens_cut = (
    cq.Workplane("YZ")
    .workplane(offset=W/2 + 0.5)
    .circle(lens_inner_r - 2)
    .extrude(lens_depth + 2)
)
result = result.cut(lens_cut)