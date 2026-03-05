import cadquery as cq

# Parameters
L = 120       # overall length
W = 40        # overall width
base_th = 3   # base plate thickness
wall_h = 15   # side wall height
wall_th = 3   # side wall thickness
back_plate_h = 23    # back plate height
plate_th = 2         # divider plate thickness
center_plate_h = 25  # center cross plate height
slider_th = 3        # slider thickness
slider_len = 20      # slider length
slider_w = W - 2*wall_th - 4  # slider width (with clearance)
rod_d = 3            # lever rod diameter
vert_rod_d = 3       # vertical rod diameter

# Base plate
base = cq.Workplane("XY").box(L, W, base_th)

# Side walls
left_wall = (
    cq.Workplane("XY")
    .transformed(offset=(0,  W/2 - wall_th/2, base_th/2))
    .box(L, wall_th, wall_h)
)
right_wall = (
    cq.Workplane("XY")
    .transformed(offset=(0, -W/2 + wall_th/2, base_th/2))
    .box(L, wall_th, wall_h)
)

# Back vertical plate inside channel
back_plate = (
    cq.Workplane("XY")
    .transformed(offset=(0, W/2 - wall_th - plate_th/2, base_th + back_plate_h/2))
    .box(L, plate_th, back_plate_h)
)

# Center cross plate at mid-length
center_plate = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, base_th + center_plate_h/2))
    .box(plate_th, W - 2*wall_th, center_plate_h)
)

# Slider block inside channel
slider = (
    cq.Workplane("XY")
    .transformed(offset=(-L/2 + slider_len/2 + 5, 0, base_th + slider_th/2))
    .box(slider_len, slider_w, slider_th)
)

# Lever rod through slider (runs along Y axis)
lever = (
    cq.Workplane("XZ")
    .transformed(offset=(-L/2 + slider_len/2 + 5, 0, base_th + slider_th/2))
    .circle(rod_d/2)
    .extrude(W + 2*wall_th)
)

# Vertical rod through base (along Z axis)
vert_rod = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, base_th/2))
    .circle(vert_rod_d/2)
    .extrude(wall_h + 10)
)

# Combine all parts
result = (
    base
    .union(left_wall)
    .union(right_wall)
    .union(back_plate)
    .union(center_plate)
    .union(slider)
    .union(lever)
    .union(vert_rod)
)