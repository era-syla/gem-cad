import cadquery as cq

# --- Parameters ---

# General alignment and scaling
overall_length = 280.0
axis_vector = (0, 0, 1)

# Emitter (Blade Holder) Section
emitter_plate_dia = 40.0
emitter_plate_thick = 3.0
emitter_pin_dia = 18.0
emitter_pin_height = 5.0
emitter_neck_narrow_dia = 12.0
emitter_neck_narrow_len = 12.0
emitter_neck_wide_dia = 28.0
emitter_neck_wide_len = 5.0
emitter_base_dia = 32.0
emitter_base_len = 8.0

# Grenade Grip Section
grenade_section_len = 70.0
grenade_outer_dia = 34.0
grenade_groove_depth = 4.0
grenade_groove_width = 3.0
grenade_rib_width = 4.0
num_ribs = 9

# Clamp/Switch Section
clamp_section_len = 60.0
clamp_dia = 36.0
clamp_box_len = 45.0
clamp_box_width = 12.0
clamp_box_height = 6.0
clamp_box_offset = clamp_section_len / 2.0

# Booster/Pommel Section
booster_section_len = 45.0
booster_dia = 38.0
pommel_gear_dia = 42.0
pommel_gear_len = 20.0
pommel_cube_size = 6.0
num_pommel_cubes = 6
pommel_cap_dia = 34.0
pommel_cap_len = 5.0

# --- Geometry Construction ---

# 1. Emitter Construction
# Start from the top (Z=0 and move negative for convenience, or build up)
# Let's build upwards from Z=0

current_z = 0.0

# The Emitter Pin (top most part)
emitter_pin = cq.Workplane("XY").workplane(offset=current_z).circle(emitter_pin_dia/2).extrude(emitter_pin_height)
current_z -= emitter_plate_thick

# The Emitter Dish/Plate
emitter_plate = cq.Workplane("XY").workplane(offset=current_z).circle(emitter_plate_dia/2).extrude(emitter_plate_thick)
current_z -= emitter_neck_narrow_len

# The Thin Neck
emitter_neck_narrow = cq.Workplane("XY").workplane(offset=current_z).circle(emitter_neck_narrow_dia/2).extrude(emitter_neck_narrow_len)
current_z -= emitter_neck_wide_len

# The Wide Neck Flange
emitter_neck_wide = cq.Workplane("XY").workplane(offset=current_z).circle(emitter_neck_wide_dia/2).extrude(emitter_neck_wide_len)
current_z -= 10.0 # Spacing for another narrow section

# Second Narrow Neck Section
emitter_neck_narrow_2 = cq.Workplane("XY").workplane(offset=current_z).circle(emitter_neck_narrow_dia/2).extrude(10.0)
current_z -= emitter_base_len

# Emitter Base (transition to grenade)
emitter_base = cq.Workplane("XY").workplane(offset=current_z).circle(emitter_base_dia/2).extrude(emitter_base_len)
current_z -= grenade_section_len

# 2. Grenade Grip Construction
# Create the main cylinder
grenade_core = cq.Workplane("XY").workplane(offset=current_z).circle(grenade_outer_dia/2).extrude(grenade_section_len)

# Create cuts for the ribs
# We will make a tool to cut the grooves
rib_pitch = grenade_section_len / num_ribs
cutter_profile = cq.Workplane("XZ").rect(grenade_outer_dia + 10, grenade_groove_width)

grenade_grip = grenade_core
for i in range(num_ribs):
    z_pos = current_z + (i * rib_pitch) + (rib_pitch/2)
    # Cut a groove
    cutter = cq.Workplane("XY").workplane(offset=z_pos).circle(grenade_outer_dia/2).circle((grenade_outer_dia/2) - grenade_groove_depth).extrude(grenade_groove_width)
    grenade_grip = grenade_grip.cut(cutter)

current_z -= clamp_section_len

# 3. Clamp Section
clamp_body = cq.Workplane("XY").workplane(offset=current_z).circle(clamp_dia/2).extrude(clamp_section_len)

# The Control Box
box_center_z = current_z + (clamp_section_len / 2.0)
control_box = (
    cq.Workplane("XY")
    .workplane(offset=box_center_z - (clamp_box_len/2))
    .center(0, (clamp_dia/2) - 2.0) # Embed slightly
    .rect(clamp_box_width, clamp_box_height * 2) # Height is radial here, make it deep enough
    .extrude(clamp_box_len)
)

# Refine control box to look like the image (rectangular prism sticking out)
real_control_box = (
    cq.Workplane("YZ")
    .workplane(offset=0) # X=0 plane
    .center((clamp_dia/2), box_center_z)
    .rect(clamp_box_height, clamp_box_len)
    .extrude(clamp_box_width/2.0, both=True) # Extrude along X
)

# Add rails/detail to control box
rail_width = 2.0
rail_height = 1.5
rail_left = (
    cq.Workplane("YZ")
    .workplane(offset=-(clamp_box_width/2))
    .center((clamp_dia/2)+clamp_box_height, box_center_z)
    .rect(rail_height, clamp_box_len)
    .extrude(rail_width)
)
rail_right = (
    cq.Workplane("YZ")
    .workplane(offset=(clamp_box_width/2) - rail_width)
    .center((clamp_dia/2)+clamp_box_height, box_center_z)
    .rect(rail_height, clamp_box_len)
    .extrude(rail_width)
)

current_z -= booster_section_len

# 4. Booster Section (Lower body)
booster = cq.Workplane("XY").workplane(offset=current_z).circle(booster_dia/2).extrude(booster_section_len)

# Add a groove near the bottom of the booster
booster_groove = (
    cq.Workplane("XY")
    .workplane(offset=current_z + 10)
    .circle(booster_dia/2 + 1)
    .circle(booster_dia/2 - 1.5)
    .extrude(3.0)
)
booster = booster.cut(booster_groove)

current_z -= pommel_gear_len

# 5. Pommel (Gear section)
pommel_core = cq.Workplane("XY").workplane(offset=current_z).circle(pommel_gear_dia/2).extrude(pommel_gear_len)

# Create the "cubes" or gear teeth
pommel_gear = pommel_core
for i in range(num_pommel_cubes):
    angle = (360.0 / num_pommel_cubes) * i
    cube = (
        cq.Workplane("XY")
        .workplane(offset=current_z)
        .transformed(rotate=(0, 0, angle))
        .center(pommel_gear_dia/2, 0)
        .rect(pommel_cube_size, pommel_cube_size * 2) # Width, Tangential width
        .extrude(pommel_gear_len)
    )
    # We want to subtract the spaces between or add bumps? Image shows bumps (cubes).
    # Actually, the image shows a larger cylinder with notches cut out, or cubes added.
    # Let's create cubes around the perimeter.
    cube_feature = (
        cq.Workplane("XY")
        .workplane(offset=current_z)
        .transformed(rotate=(0,0,angle))
        .center(pommel_gear_dia/2, 0)
        .box(pommel_cube_size*1.5, pommel_cube_size*1.5, pommel_gear_len, centered=(True, True, False))
    )
    pommel_gear = pommel_gear.union(cube_feature)

current_z -= pommel_cap_len

# 6. Pommel Cap (End piece)
pommel_cap = cq.Workplane("XY").workplane(offset=current_z).circle(pommel_cap_dia/2).extrude(pommel_cap_len)


# --- Assembly ---

# Combine all solid parts
result = (
    emitter_pin
    .union(emitter_plate)
    .union(emitter_neck_narrow)
    .union(emitter_neck_wide)
    .union(emitter_neck_narrow_2)
    .union(emitter_base)
    .union(grenade_grip)
    .union(clamp_body)
    .union(real_control_box)
    .union(rail_left)
    .union(rail_right)
    .union(booster)
    .union(pommel_gear)
    .union(pommel_cap)
)

# Rotate to match image orientation (lay flat)
result = result.rotate((0,0,0), (0,1,0), -90).rotate((0,0,0), (0,0,1), -30)