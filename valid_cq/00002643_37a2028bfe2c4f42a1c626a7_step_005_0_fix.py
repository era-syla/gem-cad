import cadquery as cq

# Main body dimensions
body_w = 60
body_h = 45
body_d = 30

# Create main body
body = (
    cq.Workplane("XY")
    .box(body_w, body_d, body_h)
)

# Add rounded edges to main body - select edges carefully
body = (
    body
    .edges("|Z")
    .fillet(3)
)

body = (
    body
    .edges("#Z")
    .fillet(2)
)

# Front face - lens area (circular depression + lens)
# Lens housing (cylindrical protrusion on front)
lens_housing = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, body_d/2, 0))
    .circle(12)
    .extrude(5)
)

# Lens inner
lens_inner = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, body_d/2 + 5, 0))
    .circle(10)
    .extrude(2)
)

# Side button (right side)
side_button = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(body_w/2, 0, 5))
    .circle(4)
    .extrude(2)
)

# Top mode button
mode_button = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(10, 0, body_h/2))
    .circle(5)
    .extrude(3)
)

# Screen recess on top
screen = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-10, -5, body_h/2))
    .rect(18, 14)
    .extrude(1)
)

# Combine main body with protrusions
result = body.union(lens_housing).union(lens_inner).union(side_button).union(mode_button)

# Cut lens detail lines (cross pattern on lens)
lens_cut_h = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, body_d/2 + 7, 0))
    .rect(20, 1)
    .extrude(1)
)

lens_cut_v = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(0, body_d/2 + 7, 0))
    .rect(1, 20)
    .extrude(1)
)

result = result.cut(lens_cut_h).cut(lens_cut_v)

# USB port cutout on left side
usb_cut = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(-body_w/2, 0, -5))
    .rect(12, 5)
    .extrude(3)
)

# HDMI port cutout on left side
hdmi_cut = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(-body_w/2, 0, 3))
    .rect(14, 4)
    .extrude(3)
)

result = result.cut(usb_cut).cut(hdmi_cut)

# Screen recess on top-back area
screen_recess = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-12, -4, body_h/2))
    .rect(16, 12)
    .extrude(2)
)

result = result.cut(screen_recess)

# Right side circular button recess
right_button_recess = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(body_w/2, 5, -5))
    .circle(5)
    .extrude(2)
)

result = result.cut(right_button_recess)

# Add small indicator circles on front face
small_circle1 = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(15, body_d/2, 10))
    .circle(3)
    .extrude(1)
)

result = result.union(small_circle1)