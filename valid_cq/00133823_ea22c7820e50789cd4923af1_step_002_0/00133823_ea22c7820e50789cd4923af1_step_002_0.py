import cadquery as cq

# --- Parameters ---
thickness = 1.0

# Left Plate Dimensions (Wider plate with corner notch)
l_width = 40.0
l_depth = 30.0
l_notch_size = 5.0
l_pos_x = -35.0  # Position in space

# Right Plate Dimensions (Narrower plate with edge tab)
r_width = 20.0
r_depth = 30.0
r_tab_width = 8.0
r_tab_protrusion = 2.5
r_tab_offset_x = 2.0  # Offset from center
r_pos_x = 25.0  # Position in space

# --- Left Object Construction ---
# A rectangle with a rectangular cutout at the top-right corner
l_pts = [
    (-l_width/2, -l_depth/2),                   # Bottom-Left
    (l_width/2, -l_depth/2),                    # Bottom-Right
    (l_width/2, l_depth/2 - l_notch_size),      # Right edge (up to notch)
    (l_width/2 - l_notch_size, l_depth/2 - l_notch_size), # Notch inner corner
    (l_width/2 - l_notch_size, l_depth/2),      # Top edge (from notch)
    (-l_width/2, l_depth/2)                     # Top-Left
]

left_plate = (
    cq.Workplane("XY")
    .polyline(l_pts)
    .close()
    .extrude(thickness)
    .translate((l_pos_x, 0, 0))
)

# --- Right Object Construction ---
# A rectangle with a tab protruding from the top (back) edge
# Calculate tab X coordinates
tab_x_right = r_tab_offset_x + r_tab_width/2
tab_x_left = r_tab_offset_x - r_tab_width/2

r_pts = [
    (-r_width/2, -r_depth/2),                   # Bottom-Left
    (r_width/2, -r_depth/2),                    # Bottom-Right
    (r_width/2, r_depth/2),                     # Top-Right
    (tab_x_right, r_depth/2),                   # Tab start
    (tab_x_right, r_depth/2 + r_tab_protrusion),# Tab outer-right
    (tab_x_left, r_depth/2 + r_tab_protrusion), # Tab outer-left
    (tab_x_left, r_depth/2),                    # Tab end
    (-r_width/2, r_depth/2)                     # Top-Left
]

right_plate = (
    cq.Workplane("XY")
    .polyline(r_pts)
    .close()
    .extrude(thickness)
    .translate((r_pos_x, 0, 0))
)

# --- Final Assembly ---
result = left_plate.union(right_plate)