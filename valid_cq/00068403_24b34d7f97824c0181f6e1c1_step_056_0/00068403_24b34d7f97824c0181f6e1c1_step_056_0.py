import cadquery as cq

# --- Dimensions and Parameters ---
plate_thickness = 2.0

# Left Panel Dimensions (The larger section with big holes)
lp_width = 160.0
lp_length = 150.0

# Right Panel Dimensions (The smaller section)
rp_width = 160.0
rp_length = 110.0

# Bridge Dimensions (Connecting neck)
bridge_width = 80.0
bridge_length = 50.0

# Hole Configurations
small_hole_dia = 3.2    # Perimeter rivets/screws
large_hole_dia = 24.0   # Large cutouts on left panel
med_hole_dia = 14.0     # Medium cutouts next to large ones
corner_hole_dia = 9.0   # Holes near the far left corners
mount_hole_dia = 5.0    # Mounting holes on the right panel

hole_pitch = 12.0       # Spacing between small perimeter holes
edge_margin = 6.0       # Margin from the edge for hole centers

# --- Geometry Construction ---

# 1. Base Geometry
# Coordinate System: Origin at the center of the bridge/neck.
# Left panel extends in -X, Right panel extends in +X.

# Create Bridge
bridge = cq.Workplane("XY").box(bridge_length, bridge_width, plate_thickness)

# Create Left Panel
# Center X position is offset by half bridge length + half panel length
lp_center_x = -(bridge_length / 2.0 + lp_length / 2.0)
left_panel = cq.Workplane("XY").box(lp_length, lp_width, plate_thickness)\
    .translate((lp_center_x, 0, 0))

# Create Right Panel
rp_center_x = (bridge_length / 2.0 + rp_length / 2.0)
right_panel = cq.Workplane("XY").box(rp_length, rp_width, plate_thickness)\
    .translate((rp_center_x, 0, 0))

# Union all parts into the base shape
base_plate = left_panel.union(bridge).union(right_panel)

# 2. Point Generation for Holes

pts_perimeter = []

# -- Left Panel Perimeter Holes --
# Top and Bottom Edges (Horizontal rows)
x_start_lp = lp_center_x - lp_length / 2.0 + edge_margin
x_end_lp = -(bridge_length / 2.0) - edge_margin
y_offset_lp = lp_width / 2.0 - edge_margin

curr_x = x_start_lp
while curr_x <= x_end_lp + 0.1:
    pts_perimeter.append((curr_x, y_offset_lp))  # Top row
    pts_perimeter.append((curr_x, -y_offset_lp)) # Bottom row
    curr_x += hole_pitch

# Left Edge (Vertical row)
y_start_lp = -(lp_width / 2.0) + edge_margin + hole_pitch
y_end_lp = (lp_width / 2.0) - edge_margin - hole_pitch
x_offset_lp = lp_center_x - lp_length / 2.0 + edge_margin

curr_y = y_start_lp
while curr_y <= y_end_lp + 0.1:
    pts_perimeter.append((x_offset_lp, curr_y))
    curr_y += hole_pitch

# -- Right Panel Perimeter Holes --
# Top and Bottom Edges only
x_start_rp = (bridge_length / 2.0) + edge_margin
x_end_rp = rp_center_x + rp_length / 2.0 - edge_margin
y_offset_rp = rp_width / 2.0 - edge_margin

curr_x = x_start_rp
while curr_x <= x_end_rp + 0.1:
    pts_perimeter.append((curr_x, y_offset_rp))  # Top row
    pts_perimeter.append((curr_x, -y_offset_rp)) # Bottom row
    curr_x += hole_pitch

# -- Internal Hole Patterns --
# Defined relative to the coordinate system established above

# Row Y coordinate for internal left panel holes
internal_row_y = 50.0

# Large Holes (Closest to bridge on left panel)
large_x = -(bridge_length / 2.0 + 40.0)
pts_large = [(large_x, internal_row_y), (large_x, -internal_row_y)]

# Medium Holes (Next to large holes)
med_x = large_x - 35.0
pts_med = [(med_x, internal_row_y), (med_x, -internal_row_y)]

# Corner Holes (Far left of left panel)
corner_x = lp_center_x - lp_length / 2.0 + 30.0
pts_corner = [(corner_x, internal_row_y), (corner_x, -internal_row_y)]

# Right Panel Mounting Holes
mount_x = rp_center_x + 10.0
mount_y = 45.0
pts_mount = [(mount_x, mount_y), (mount_x, -mount_y)]

# 3. Operations
# Apply all holes to the base plate
result = base_plate.faces(">Z").workplane() \
    .pushPoints(pts_perimeter).hole(small_hole_dia) \
    .pushPoints(pts_large).hole(large_hole_dia) \
    .pushPoints(pts_med).hole(med_hole_dia) \
    .pushPoints(pts_corner).hole(corner_hole_dia) \
    .pushPoints(pts_mount).hole(mount_hole_dia)
