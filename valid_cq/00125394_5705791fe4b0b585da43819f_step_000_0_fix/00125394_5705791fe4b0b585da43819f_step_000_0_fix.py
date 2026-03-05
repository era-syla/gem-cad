import cadquery as cq

# Dimensions
width = 67.1
height = 138.3
thk = 7.1

# Create main body
result = cq.Workplane("XY").rect(width, height).extrude(thk)

# Round all edges
result = result.edges().fillet(4)

# Back face features: camera holes
cam_r = 3.0
cam_sep = 12.0
cam_offset_x = -width/2 + 12.0
cam_offset_y = height/2 - 12.0
# First lens
result = result.faces(">Z").workplane().center(cam_offset_x, cam_offset_y).circle(cam_r).cutBlind(-2.0)
# Second lens / flash
result = result.faces(">Z").workplane().center(cam_offset_x + cam_sep, cam_offset_y).circle(cam_r).cutBlind(-2.0)

# Antenna grooves
groove_w = 1.0
groove_l = width - 4.0
groove_depth = 0.5
groove_y = height/2 - 2.0
result = result.faces(">Z").workplane().center(0, groove_y).rect(groove_l, groove_w).cutBlind(-groove_depth)
result = result.faces(">Z").workplane().center(0, -groove_y).rect(groove_l, groove_w).cutBlind(-groove_depth)

# Simple logo recess
logo_r = 6.0
result = result.faces(">Z").workplane().circle(logo_r).cutBlind(-0.5)

# Side buttons
button_depth = 0.8
button_w = 2.0
button_h = 12.0
button_z = thk/2

# Power button on right
btn1 = (
    cq.Workplane("YZ")
    .rect(button_w, button_h)
    .extrude(button_depth)
    .translate((width/2, 20, button_z))
)
result = result.union(btn1)

# Volume up on left
btn2 = (
    cq.Workplane("YZ")
    .rect(button_w, button_h)
    .extrude(-button_depth)
    .translate((-width/2, 10, button_z))
)
result = result.union(btn2)

# Volume down on left
btn3 = (
    cq.Workplane("YZ")
    .rect(button_w, button_h)
    .extrude(-button_depth)
    .translate((-width/2, -10, button_z))
)
result = result.union(btn3)