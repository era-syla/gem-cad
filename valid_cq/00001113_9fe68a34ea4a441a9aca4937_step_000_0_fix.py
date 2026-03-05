import cadquery as cq

# iPhone-like smartphone model
# Dimensions roughly based on iPhone 6: 138.1 x 67 x 6.9 mm

length = 138.0
width = 67.0
thickness = 7.0
corner_r = 10.0

# Main body with rounded corners
body = (
    cq.Workplane("XY")
    .rect(width, length)
    .extrude(thickness)
)

# Apply fillets to vertical edges (corners)
body = (
    body
    .edges("|Z")
    .fillet(corner_r)
)

# Apply smaller fillets to top and bottom edges
body = (
    body
    .edges("not |Z")
    .fillet(1.5)
)

# Screen recess on front face
screen_w = 56.0
screen_l = 98.0
screen_depth = 0.5

screen_recess = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .rect(screen_w, screen_l)
    .extrude(-screen_depth)
)

body = body.cut(screen_recess)

# Home button on front face (bottom area)
home_btn = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .center(0, -length/2 + 12)
    .circle(4.5)
    .extrude(-0.6)
)

body = body.cut(home_btn)

# Front camera / earpiece area (top)
earpiece = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .center(0, length/2 - 14)
    .rect(20, 3)
    .extrude(-0.5)
)

body = body.cut(earpiece)

# Front camera small circle
front_cam = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .center(-14, length/2 - 14)
    .circle(2)
    .extrude(-0.5)
)

body = body.cut(front_cam)

# Lightning connector on bottom edge
lightning = (
    cq.Workplane("XZ")
    .workplane(offset=-length/2)
    .center(0, thickness/2)
    .rect(9, 3)
    .extrude(-2)
)

body = body.cut(lightning)

# Headphone jack on bottom edge
headphone = (
    cq.Workplane("XZ")
    .workplane(offset=-length/2)
    .center(-20, thickness/2)
    .circle(1.75)
    .extrude(-2)
)

body = body.cut(headphone)

# Volume buttons on left side
vol_up = (
    cq.Workplane("YZ")
    .workplane(offset=-width/2)
    .center(30, thickness/2)
    .rect(12, 3)
    .extrude(-1.5)
)

body = body.cut(vol_up)

vol_down = (
    cq.Workplane("YZ")
    .workplane(offset=-width/2)
    .center(12, thickness/2)
    .rect(12, 3)
    .extrude(-1.5)
)

body = body.cut(vol_down)

# Mute/silent switch on left side
mute_switch = (
    cq.Workplane("YZ")
    .workplane(offset=-width/2)
    .center(50, thickness/2)
    .rect(8, 3)
    .extrude(-1.5)
)

body = body.cut(mute_switch)

# Power button on right side
power_btn = (
    cq.Workplane("YZ")
    .workplane(offset=width/2)
    .center(30, thickness/2)
    .rect(14, 3)
    .extrude(-1.5)
)

body = body.cut(power_btn)

result = body