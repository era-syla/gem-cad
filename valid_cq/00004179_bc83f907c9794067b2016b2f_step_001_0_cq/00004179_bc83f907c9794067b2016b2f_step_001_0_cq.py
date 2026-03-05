import cadquery as cq

# --- Dimensions and Parameters ---
# Main walls
wall_thickness = 10.0
room_width = 150.0
room_length = 200.0
room_height = 100.0
back_wall_length = 250.0  # Extended back wall

# Large Cylinder (Tank)
tank_diameter = 80.0
tank_radius = tank_diameter / 2.0
tank_height = 70.0

# Front Block (Control unit?)
front_block_width = 40.0
front_block_length = 80.0
front_block_height = 60.0

# Upper Chute/Duct (Top right)
chute_width = 40.0
chute_length = 100.0
chute_wall_thick = 5.0

# Piping/Ladder assembly
pipe_radius = 2.0
ladder_rung_spacing = 10.0
ladder_width = 25.0

# Doorway
door_width = 25.0
door_height = 40.0

# --- Geometry Construction ---

# 1. Main Structural Walls
# Back Wall
back_wall = (
    cq.Workplane("XY")
    .box(back_wall_length, wall_thickness, room_height)
    .translate((0, room_width/2, room_height/2))
)

# Side Wall (Right)
side_wall_right = (
    cq.Workplane("XY")
    .box(wall_thickness, room_width, room_height)
    .translate((room_length/2 - wall_thickness/2, 0, room_height/2))
)

# Cut doorway in side wall
door_cutout = (
    cq.Workplane("XZ")
    .rect(door_width, door_height)
    .extrude(wall_thickness * 2)
    .translate((room_length/2 - wall_thickness/2, door_height/2, -room_width/4)) # Rough positioning based on image
    .rotate((0,0,0), (0,1,0), 90) # Correct orientation
    .rotate((0,0,0), (0,0,1), 90)
)
# Re-orient simply based on global coords
door_solid = (
    cq.Workplane("XY")
    .box(wall_thickness * 2, door_width, door_height)
    .translate((room_length/2 - wall_thickness/2, -room_width/3, door_height/2))
)

side_wall_right = side_wall_right.cut(door_solid)

# Partition Wall (Middle)
partition_wall = (
    cq.Workplane("XY")
    .box(wall_thickness, room_width/2, room_height)
    .translate((0, 0, room_height/2)) # Centered on X, extending +Y from origin roughly
    .translate((0, room_width/4, 0)) # Shift to connect to back wall
)

# 2. Large Cylindrical Tank
tank = (
    cq.Workplane("XY")
    .circle(tank_radius)
    .extrude(tank_height)
    .translate((-room_length/4, -room_width/6, 0))
)

# 3. Front Rectangular Block
front_block = (
    cq.Workplane("XY")
    .box(front_block_length, front_block_width, front_block_height)
    .translate((-room_length/3 - 10, -room_width/2 + front_block_width/2, front_block_height/2))
)

# 4. Upper Duct/Chute (Top Right)
# Outer box
chute_outer = (
    cq.Workplane("XY")
    .box(chute_length, chute_width, room_height) # Full height for now
    .translate((room_length/4 + 10, room_width/2 + chute_width/2, room_height/2))
)

# Inner cut for chute
chute_cut = (
    cq.Workplane("XY")
    .box(chute_length - chute_wall_thick*2, chute_width - chute_wall_thick*2, room_height)
    .translate((room_length/4 + 10, room_width/2 + chute_width/2, room_height/2))
)

chute = chute_outer.cut(chute_cut)

# However, looking at the image, the chute is actually part of the wall structure or behind it.
# Let's adjust to match the "L" shape on top.
# It looks like a rectangular containment area on top of the ceiling or extending back.
# Let's model the specific box visible at the top right behind the partition.
upper_chute_box = (
    cq.Workplane("XY")
    .box(room_length/2 - wall_thickness, chute_width, 20) # Only the rim visible
    .translate((room_length/4, room_width/2 + chute_width/2, room_height - 10))
)
# Create the hollow
upper_chute_hollow = (
     cq.Workplane("XY")
    .box(room_length/2 - wall_thickness - 4, chute_width - 4, 20)
    .translate((room_length/4, room_width/2 + chute_width/2, room_height - 10))
)
upper_chute = upper_chute_box.cut(upper_chute_hollow)


# 5. Piping and Detail Cluster (Above Tank)
# Small box on wall
small_box_size = 20.0
wall_box = (
    cq.Workplane("XY")
    .box(small_box_size, small_box_size, small_box_size)
    .translate((-10, room_width/2 - wall_thickness/2 - small_box_size/2, tank_height + 15))
)

# Vertical Pipe
v_pipe = (
    cq.Workplane("XY")
    .circle(pipe_radius)
    .extrude(40)
    .translate((-25, room_width/2 - wall_thickness - 5, tank_height))
)

# Horizontal Pipe run
h_pipe_path = (
    cq.Workplane("YZ")
    .moveTo(tank_height + 30, room_width/2 - wall_thickness - 5)
    .lineTo(tank_height + 30, room_width/2 - wall_thickness - 40)
    .lineTo(tank_height + 10, room_width/2 - wall_thickness - 40)
)
# This is complex to sweep simply without a proper path object, using simple cylinders instead
h_pipe1 = (
    cq.Workplane("XY")
    .cylinder(40, pipe_radius, centered=False)
    .rotate((0,0,0), (0,0,1), -90)
    .translate((-25, room_width/2 - wall_thickness - 5, tank_height + 35))
)
v_pipe_drop = (
    cq.Workplane("XY")
    .cylinder(25, pipe_radius, centered=False)
    .translate((-25, room_width/2 - wall_thickness - 45, tank_height + 10))
)

# Parallel Rungs/Ladder structure angled into tank
rung_length = 50.0
rung_angle = 45.0

ladder_leg_1 = (
    cq.Workplane("YZ")
    .rect(2, 60)
    .extrude(2)
    .rotate((0,0,0), (1,0,0), -30)
    .translate((0, 0, tank_height + 10))
)

ladder_assy = cq.Assembly()

# Create angled struts going into the tank
strut_geo = cq.Workplane("XY").box(60, 2, 2).rotate((0,0,0),(0,1,0), -30) # Angled down
strut1 = strut_geo.translate((-10, 0, tank_height + 10))
strut2 = strut_geo.translate((10, 0, tank_height + 10))
strut3 = strut_geo.translate((30, 0, tank_height + 10))

# Create horizontal grating/pipes near the wall box
grating = cq.Workplane("XY").box(40, 15, 2).translate((-35, room_width/2 - 30, tank_height + 10))


# --- Combine All Parts ---

result = (
    back_wall
    .union(side_wall_right)
    .union(partition_wall)
    .union(tank)
    .union(front_block)
    .union(upper_chute)
    .union(wall_box)
    .union(v_pipe)
    .union(h_pipe1)
    .union(v_pipe_drop)
    .union(strut1)
    .union(strut2)
    .union(strut3)
    .union(grating)
)

# Add a floor plate for visual grounding (optional, but helps context)
floor = (
    cq.Workplane("XY")
    .box(room_length + 20, room_width + 20, 2)
    .translate((0, 0, -1))
)
# result = result.union(floor) # Excluded based on strict interpretation of visible gray mass

# Export or Render
if 'show_object' in globals():
    show_object(result)