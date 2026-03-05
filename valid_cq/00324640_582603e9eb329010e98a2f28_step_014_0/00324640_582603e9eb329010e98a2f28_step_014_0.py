import cadquery as cq

# --- Dimensions & Parameters ---

# Gearbox (Main Housing)
gb_length = 46.0
gb_width = 32.0
gb_height = 25.0
gb_fillet = 2.5
gb_color = (0.5, 0.5, 0.5)

# Motor (Rear Section)
motor_dia = 24.4
motor_len = 31.0
motor_flat_h = 18.2  # Height between flat sides
motor_rear_boss_dia = 6.2
motor_rear_boss_h = 2.0
motor_top_nub_dim = (6.0, 5.0, 1.5) # LxWxH

# Output Shaft
shaft_dia = 6.0
shaft_len = 14.0
shaft_pos_x_offset = 11.0  # Distance from front face
shaft_boss_dia = 12.0
shaft_boss_h = 1.2
shaft_d_cut_depth = 0.5

# Alignment Pin
pin_dia = 3.0
pin_h = 3.0
pin_dist_from_shaft = 9.0

# Mounting Holes
hole_dia = 3.0
hole_depth = 10.0
hole_spacing_x = 34.0
hole_spacing_y = 22.0

# --- Geometry Construction ---

# 1. Main Gearbox Body
# Centered on origin, so Z ranges from -gb_height/2 to +gb_height/2
gearbox = (
    cq.Workplane("XY")
    .box(gb_length, gb_width, gb_height)
    .edges("|Z")
    .fillet(gb_fillet)
)

# Add Mounting Holes on top face
gearbox = (
    gearbox.faces(">Z")
    .workplane()
    .rect(hole_spacing_x, hole_spacing_y)
    .vertices()
    .hole(hole_dia, depth=hole_depth)
)

# 2. Motor Assembly
# Attached to the -X face of the gearbox
# Motor axis aligns with X axis, centered at Z=0, Y=0

# Base Cylinder
motor = (
    cq.Workplane("YZ")
    .workplane(offset=-gb_length/2.0)
    .circle(motor_dia/2.0)
    .extrude(-motor_len)
)

# Cut Flats (Top and Bottom)
# We cut material to achieve the flat height
cut_h = (motor_dia - motor_flat_h) / 2.0
cut_w = motor_dia + 5.0 # Wider than diameter to ensure clean cut

# Top Cut
motor = motor.cut(
    cq.Workplane("YZ")
    .workplane(offset=-gb_length/2.0)
    .center(0, motor_flat_h/2.0 + cut_h/2.0 + 0.01)
    .rect(cut_w, cut_h + 0.02)
    .extrude(-motor_len)
)

# Bottom Cut
motor = motor.cut(
    cq.Workplane("YZ")
    .workplane(offset=-gb_length/2.0)
    .center(0, -(motor_flat_h/2.0 + cut_h/2.0 + 0.01))
    .rect(cut_w, cut_h + 0.02)
    .extrude(-motor_len)
)

# Chamfer the rear edge of the motor for the end-cap look
motor = motor.edges("<X").chamfer(1.0)

# Motor Rear Boss
motor_rear = (
    cq.Workplane("YZ")
    .workplane(offset=-(gb_length/2.0 + motor_len))
    .circle(motor_rear_boss_dia/2.0)
    .extrude(-motor_rear_boss_h)
)

# Small detail nub on top of motor
motor_nub = (
    cq.Workplane("XY")
    .workplane(offset=motor_flat_h/2.0) # Sits on the top flat
    .center(-(gb_length/2.0 + 6.0), 0)
    .rect(motor_top_nub_dim[0], motor_top_nub_dim[1])
    .extrude(motor_top_nub_dim[2])
)

# 3. Output Shaft Assembly
# Located on the top face of the gearbox (>Z)
shaft_x = (gb_length / 2.0) - shaft_pos_x_offset
shaft_y = 0
top_z = gb_height / 2.0

# Shaft Boss
shaft_boss = (
    cq.Workplane("XY")
    .workplane(offset=top_z)
    .center(shaft_x, shaft_y)
    .circle(shaft_boss_dia/2.0)
    .extrude(shaft_boss_h)
)

# Main Shaft Cylinder
shaft = (
    cq.Workplane("XY")
    .workplane(offset=top_z + shaft_boss_h)
    .center(shaft_x, shaft_y)
    .circle(shaft_dia/2.0)
    .extrude(shaft_len)
)

# D-Cut (Flat section on shaft)
# Remove material from one side (e.g., +Y side)
d_cut_offset = (shaft_dia/2.0) - shaft_d_cut_depth
shaft = shaft.cut(
    cq.Workplane("XY")
    .workplane(offset=top_z + shaft_boss_h)
    .center(shaft_x, shaft_y + d_cut_offset + 5.0)
    .rect(shaft_dia*2, 10.0)
    .extrude(shaft_len)
)

# 4. Alignment Pin
# Located behind the shaft
pin_x = shaft_x - pin_dist_from_shaft
pin = (
    cq.Workplane("XY")
    .workplane(offset=top_z)
    .center(pin_x, 0)
    .circle(pin_dia/2.0)
    .extrude(pin_h)
)

# --- Final Assembly ---
result = (
    gearbox
    .union(motor)
    .union(motor_rear)
    .union(motor_nub)
    .union(shaft_boss)
    .union(shaft)
    .union(pin)
)