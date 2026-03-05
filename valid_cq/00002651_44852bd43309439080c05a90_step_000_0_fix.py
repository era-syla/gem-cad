import cadquery as cq

# Main dimensions
base_w = 160
base_d = 120
base_h = 8

# Build the main top platform/box
top_box = cq.Workplane("XY").box(base_w, base_d, base_h)

# Legs/feet - rectangular blocks under the platform
leg_w = 20
leg_d = base_d
leg_h = 30

# Two legs side by side under the front portion
leg1 = cq.Workplane("XY").box(leg_w, leg_d, leg_h).translate((-base_w/2 + leg_w/2, 0, -leg_h/2 - base_h/2))
leg2 = cq.Workplane("XY").box(leg_w, leg_d, leg_h).translate((base_w/2 - leg_w/2, 0, -leg_h/2 - base_h/2))

# Channel/duct structure - wide flat box under the main platform between legs
channel_w = base_w - 2*leg_w
channel_d = base_d
channel_h = leg_h
channel = cq.Workplane("XY").box(channel_w, channel_d, channel_h).translate((0, 0, -channel_h/2 - base_h/2))

# Divider in the channel
divider_w = 4
divider = cq.Workplane("XY").box(divider_w, channel_d, channel_h).translate((0, 0, -channel_h/2 - base_h/2))

# Back wall panel
back_wall_w = base_w + 20
back_wall_h = 60
back_wall_t = 4
back_wall = cq.Workplane("XY").box(back_wall_w, back_wall_t, back_wall_h).translate((0, -base_d/2 - back_wall_t/2, back_wall_h/2 - base_h/2 - leg_h/2))

# Side panel on right
side_panel_d = base_d + back_wall_t
side_panel_h = back_wall_h
side_panel_t = 4
side_panel = cq.Workplane("XY").box(side_panel_t, side_panel_d, side_panel_h).translate((base_w/2 + side_panel_t/2, -back_wall_t/2, side_panel_h/2 - base_h/2 - leg_h/2))

# Antenna - thin rod
antenna_r = 1
antenna_h = 80
antenna = cq.Workplane("XY").cylinder(antenna_h, antenna_r).translate((-base_w/4, base_d/4, base_h/2 + antenna_h/2))

# Channel openings - cut openings in the channel front face
# Left opening
opening_w = (channel_w - divider_w)/2 - 4
opening_h = channel_h - 8
left_opening = cq.Workplane("XY").box(opening_w, channel_d + 10, opening_h).translate((-opening_w/2 - divider_w/2, 0, -channel_h/2 - base_h/2))
right_opening = cq.Workplane("XY").box(opening_w, channel_d + 10, opening_h).translate((opening_w/2 + divider_w/2, 0, -channel_h/2 - base_h/2))

# Build channel box and cut openings
channel_solid = channel.union(divider)
channel_with_openings = channel_solid.cut(left_opening).cut(right_opening)

# Combine everything
result = (top_box
    .union(leg1)
    .union(leg2)
    .union(channel_with_openings)
    .union(back_wall)
    .union(side_panel)
    .union(antenna)
)