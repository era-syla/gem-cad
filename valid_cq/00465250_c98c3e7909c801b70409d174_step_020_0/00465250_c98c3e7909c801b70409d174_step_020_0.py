import cadquery as cq

# --- Parameters ---
thickness = 1.0

# Main Panel Dimensions
center_width = 80.0
center_height_top = 110.0    # Height from wing bottom reference line
center_height_bottom = 15.0  # Extension below wing bottom reference line
wing_width = 50.0
wing_height = 75.0
chamfer_size = 15.0          # Size of the chamfer at wing/center junction

# Feature Parameters
fold_cut_width = 0.5
v_dash_len = 6.0
v_dash_gap = 4.0
h_dash_len = 8.0
h_dash_gap = 5.0

slot_length = 8.0
slot_width = 3.5
slot_offset_x = 12.0  # Distance from outer wing edge
slot_offset_y = 12.0  # Distance from wing bottom edge

# --- Calculations ---
x_center_half = center_width / 2.0
x_wing_outer = x_center_half + wing_width
y_bot = -center_height_bottom
y_wing_bot = 0.0
y_wing_top = wing_height
y_top = center_height_top

# --- Geometry Construction ---

# 1. Define the Outline Profile
# Points are defined Counter-Clockwise starting from bottom-center
pts = [
    (0, y_bot),                           # Start center bottom
    (x_center_half, y_bot),               # Bottom right center corner
    (x_center_half, y_wing_bot),          # Wing connection corner
    (x_wing_outer, y_wing_bot),           # Wing bottom right
    (x_wing_outer, y_wing_top),           # Wing top right
    (x_center_half + chamfer_size, y_wing_top), # Chamfer start on wing top
    (x_center_half, y_wing_top - chamfer_size), # Chamfer end on fold line
    (x_center_half, y_top),               # Top right center
    (-x_center_half, y_top),              # Top left center
    (-x_center_half, y_wing_top - chamfer_size),# Chamfer start left
    (-x_center_half - chamfer_size, y_wing_top),# Chamfer end left
    (-x_wing_outer, y_wing_top),          # Wing top left
    (-x_wing_outer, y_wing_bot),          # Wing bottom left
    (-x_center_half, y_wing_bot),         # Wing connection corner left
    (-x_center_half, y_bot),              # Bottom left center corner
]

# Create the base solid
result = cq.Workplane("XY").polyline(pts).close().extrude(thickness)

# 2. Create Vertical Fold Perforations
# Located along x = +/- x_center_half
v_dash_pts = []
y_curr = y_wing_bot + 3.0 # Start with a small offset
y_limit = y_wing_top - chamfer_size

while y_curr + v_dash_len < y_limit:
    # Add points for left and right fold lines
    # Using center of the dash rect
    cy = y_curr + v_dash_len / 2.0
    v_dash_pts.append((x_center_half, cy))
    v_dash_pts.append((-x_center_half, cy))
    y_curr += v_dash_len + v_dash_gap

if v_dash_pts:
    result = result.faces(">Z").workplane() \
        .pushPoints(v_dash_pts) \
        .rect(fold_cut_width, v_dash_len) \
        .cutThruAll()

# 3. Create Horizontal Fold Perforations
# Located on the top section of the center panel
h_dash_pts = []
row_y_coords = [y_wing_top + 10.0, y_wing_top + 22.0]

# Calculate centering for dashes
# Assume 4 dashes across the width
num_h_dashes = 4
h_pitch = h_dash_len + h_dash_gap
total_span = (num_h_dashes * h_dash_len) + ((num_h_dashes - 1) * h_dash_gap)
start_x = -total_span / 2.0 + h_dash_len / 2.0

for ry in row_y_coords:
    for i in range(num_h_dashes):
        cx = start_x + i * h_pitch
        h_dash_pts.append((cx, ry))

if h_dash_pts:
    result = result.faces(">Z").workplane() \
        .pushPoints(h_dash_pts) \
        .rect(h_dash_len, fold_cut_width) \
        .cutThruAll()

# 4. Create Slots on Wings
slot_cx = x_wing_outer - slot_offset_x - slot_length/2.0
slot_cy = y_wing_bot + slot_offset_y
slot_pts = [
    (slot_cx, slot_cy),
    (-slot_cx, slot_cy)
]

result = result.faces(">Z").workplane() \
    .pushPoints(slot_pts) \
    .slot2D(slot_length, slot_width, 0) \
    .cutThruAll()