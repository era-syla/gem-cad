import cadquery as cq
import math

# --- Parameters ---

# Head Tube
ht_length = 120
ht_diameter = 44
ht_wall = 4
ht_angle = 70  # Degrees from horizontal

# Seat Tube
st_length = 400
st_diameter = 31.6
st_wall = 2.5
st_angle = 73  # Degrees from horizontal

# Bottom Bracket Shell
bb_width = 73
bb_diameter = 40
bb_wall = 3.5

# Tube Profiles
tt_diameter = 38
dt_diameter = 42
tube_wall = 2.0

# Frame Geometry (Approximate based on image)
# Coordinates relative to BB center (0,0,0)
bb_center = (0, 0, 0)

# Calculate Seat Tube Top Position
st_top_x = -st_length * math.cos(math.radians(st_angle))
st_top_y = st_length * math.sin(math.radians(st_angle))
st_top = (st_top_x, st_top_y, 0)

# Calculate Head Tube Center Position (Reach and Stack approximation)
reach = 380
stack = 500
ht_center_x = reach
ht_center_y = stack
ht_center = (ht_center_x, ht_center_y, 0)

# --- Components Construction ---

# 1. Bottom Bracket Shell (BB)
# Cylindrical shell along the Z-axis (width direction usually in bike frames, but let's align Y for height, X for length, Z for width)
# Re-orienting: X=Length, Y=Height, Z=Width
# The image shows an isometric view. Let's build flat on XY plane and extrude/shell or use pipes.

# Let's define the BB shell oriented along the Z axis
bb_shell = (
    cq.Workplane("XY")
    .circle(bb_diameter / 2 + bb_wall)
    .circle(bb_diameter / 2)
    .extrude(bb_width / 2)
    .union(
        cq.Workplane("XY")
        .circle(bb_diameter / 2 + bb_wall)
        .circle(bb_diameter / 2)
        .extrude(-bb_width / 2)
    )
)

# 2. Seat Tube (ST)
# Cylinder angled up from BB area
st_plane = cq.Workplane("XY").transformed(offset=(st_top_x, st_top_y, 0), rotate=(0, 0, -90 + st_angle))

seat_tube = (
    cq.Workplane("XY")
    .transformed(offset=(0,0,0), rotate=(0, 0, 180-st_angle)) # Align with ST angle
    .workplane(offset=-20) # Start slightly below BB center for welding
    .circle(st_diameter / 2 + st_wall)
    .circle(st_diameter / 2)
    .extrude(st_length + 40) # Extrude past the theoretical top
)

# 3. Head Tube (HT)
# Cylinder located at reach/stack, angled
ht_plane = cq.Workplane("XY").transformed(offset=(ht_center_x, ht_center_y, 0), rotate=(0, 0, -90 + ht_angle))

head_tube_outer = (
    cq.Workplane("XY")
    .transformed(offset=(ht_center_x, ht_center_y, 0), rotate=(0, 0, -ht_angle))
    .circle(ht_diameter / 2 + ht_wall)
    .extrude(ht_length / 2, both=True)
)

# Add "cups" or reinforcement rings to headtube ends
ht_cup = (
    cq.Workplane("XY")
    .transformed(offset=(ht_center_x, ht_center_y, 0), rotate=(0, 0, -ht_angle))
    .circle(ht_diameter / 2 + ht_wall + 2)
    .extrude(8)
)
ht_cup_bottom = (
    cq.Workplane("XY")
    .transformed(offset=(ht_center_x, ht_center_y, 0), rotate=(0, 0, -ht_angle))
    .workplane(offset=-ht_length/2)
    .circle(ht_diameter / 2 + ht_wall + 2)
    .extrude(-8)
)

head_tube = head_tube_outer.union(ht_cup).union(ht_cup_bottom)
# Cut the bore
head_tube = head_tube.cut(
    cq.Workplane("XY")
    .transformed(offset=(ht_center_x, ht_center_y, 0), rotate=(0, 0, -ht_angle))
    .circle(ht_diameter / 2)
    .extrude(ht_length / 2 + 10, both=True)
)

# 4. Top Tube (TT)
# Connects HT to ST. Needs a curve.
# Points: Near top of HT, Near top of ST.

# Define attachment points on surface of HT and ST
tt_start_node = (ht_center_x - (ht_diameter/2)*math.sin(math.radians(ht_angle)), 
                 ht_center_y - 20, 0)
tt_end_node = (st_top_x + 10, st_top_y - 30, 0)

# Create a bent path for the top tube (hydroformed look)
tt_path = (
    cq.Workplane("XY")
    .moveTo(tt_start_node[0], tt_start_node[1])
    .spline([
        (tt_start_node[0] - 100, tt_start_node[1] - 10), # Control point
        (tt_end_node[0] + 50, tt_end_node[1] - 20),      # Control point
        (tt_end_node[0], tt_end_node[1])
    ], includeCurrent=True)
)

top_tube = (
    cq.Workplane("YZ")
    .workplane(offset=tt_start_node[0])
    .moveTo(0, tt_start_node[1]) # Adjust local coords
    .circle(tt_diameter / 2)
    .sweep(tt_path)
)
# Hollow out TT (simplified)
top_tube_inner = (
    cq.Workplane("YZ")
    .workplane(offset=tt_start_node[0])
    .moveTo(0, tt_start_node[1])
    .circle(tt_diameter / 2 - tube_wall)
    .sweep(tt_path)
)
top_tube = top_tube.cut(top_tube_inner)

# 5. Down Tube (DT)
# Connects HT to BB/ST junction.
dt_start_node = (ht_center_x - (ht_diameter/2)*math.sin(math.radians(ht_angle)), 
                 ht_center_y - ht_length/2 + 10, 0)
dt_end_node = (20, 20, 0) # Near BB, slight offset up

# Create a bent path for the down tube (clearance for fork/wheel)
dt_path = (
    cq.Workplane("XY")
    .moveTo(dt_start_node[0], dt_start_node[1])
    .spline([
        (dt_start_node[0] - 50, dt_start_node[1] - 60),
        (dt_end_node[0] + 80, dt_end_node[1] + 80),
        (dt_end_node[0], dt_end_node[1])
    ], includeCurrent=True)
)

down_tube = (
    cq.Workplane("YZ")
    .workplane(offset=dt_start_node[0])
    .moveTo(0, dt_start_node[1])
    .circle(dt_diameter / 2)
    .sweep(dt_path)
)

# Hollow out DT
down_tube_inner = (
    cq.Workplane("YZ")
    .workplane(offset=dt_start_node[0])
    .moveTo(0, dt_start_node[1])
    .circle(dt_diameter / 2 - tube_wall)
    .sweep(dt_path)
)
down_tube = down_tube.cut(down_tube_inner)


# 6. Linkage Mounts (Pivot points)
# One on Seat Tube, one lower down near BB/DT junction

# Upper Mount (Shock Mount)
mount_width = 15
mount_height = 40
mount_thick = 10
mount_pos_y = st_top_y - 150
mount_pos_x = st_top_x + (mount_pos_y / math.tan(math.radians(st_angle))) + 35 # Rough calc to be on tube

upper_mount_base = (
    cq.Workplane("YZ")
    .workplane(offset=mount_pos_x)
    .moveTo(0, mount_pos_y)
    .rect(25, 50)
    .extrude(30)
)
# Sculpt the mount
upper_mount = (
    upper_mount_base
    .faces(">X").workplane()
    .hole(8) # Bolt hole
    .faces(">X").workplane()
    .rect(10, 60).cutBlind(-15) # Slot for shock eyelet
)

# Lower Mount (Main Pivot)
lower_mount_pos_x = 25
lower_mount_pos_y = 60
lower_mount = (
    cq.Workplane("XY")
    .transformed(offset=(lower_mount_pos_x, lower_mount_pos_y, 0), rotate=(0,0,0))
    .box(30, 40, 25)
    .faces(">Z").workplane()
    .hole(10) # Pivot hole
    .faces(">X").workplane()
    .rect(15, 50).cutBlind(-15) # Slot
)


# --- Assembly ---

# Union everything
frame = bb_shell.union(seat_tube).union(head_tube).union(top_tube).union(down_tube)

# Clean up overlaps (Simple boolean union handles this visual merging)
frame = frame.union(upper_mount)
frame = frame.union(lower_mount)

# Apply Fillets to smooth transitions (Welds/Hydroforming simulation)
# This is computationally expensive and prone to failure on complex intersections in kernels,
# so we apply selectively where robust.

try:
    # Try to fillet the Head Tube junctions
    frame = frame.edges("|Z").fillet(2) 
except:
    pass

result = frame
