import cadquery as cq

# --- Parameters ---
chair_width = 400.0
chair_depth = 400.0
seat_height = 450.0     # Floor to top of seat
seat_thickness = 40.0
leg_size = 40.0         # Square profile of legs
back_height = 400.0     # Extension above seat
top_bar_height = 120.0  # Height of the top horizontal bar of the backrest

# --- Geometry Construction ---

# 1. Seat
# Positioned so the top surface is at seat_height
# The seat is a simple rectangular box.
seat = (
    cq.Workplane("XY")
    .box(chair_width, chair_depth, seat_thickness)
    .translate((0, 0, seat_height - seat_thickness / 2))
)

# 2. Front Legs
# These sit under the front corners of the seat.
front_leg_height = seat_height - seat_thickness
front_leg_geo = cq.Workplane("XY").box(leg_size, leg_size, front_leg_height)

# Calculate positions for front legs (Front is -Y, Left is -X, Right is +X)
fl_pos = (-chair_width/2 + leg_size/2, -chair_depth/2 + leg_size/2, front_leg_height/2)
fr_pos = (chair_width/2 - leg_size/2, -chair_depth/2 + leg_size/2, front_leg_height/2)

front_left_leg = front_leg_geo.translate(fl_pos)
front_right_leg = front_leg_geo.translate(fr_pos)

# 3. Back Legs / Uprights
# These extend from the floor all the way to the top of the backrest.
total_back_height = seat_height + back_height
back_leg_geo = cq.Workplane("XY").box(leg_size, leg_size, total_back_height)

# Calculate positions for back legs (Back is +Y)
bl_pos = (-chair_width/2 + leg_size/2, chair_depth/2 - leg_size/2, total_back_height/2)
br_pos = (chair_width/2 - leg_size/2, chair_depth/2 - leg_size/2, total_back_height/2)

back_left_leg = back_leg_geo.translate(bl_pos)
back_right_leg = back_leg_geo.translate(br_pos)

# 4. Backrest Top Bar
# Connects the two back legs at the top.
# Width fits exactly between the two back legs.
bar_width = chair_width - 2 * leg_size
top_bar = (
    cq.Workplane("XY")
    .box(bar_width, leg_size, top_bar_height)
    .translate((
        0, 
        chair_depth/2 - leg_size/2, 
        total_back_height - top_bar_height/2
    ))
)

# --- Final Assembly ---
result = (
    seat
    .union(front_left_leg)
    .union(front_right_leg)
    .union(back_left_leg)
    .union(back_right_leg)
    .union(top_bar)
)