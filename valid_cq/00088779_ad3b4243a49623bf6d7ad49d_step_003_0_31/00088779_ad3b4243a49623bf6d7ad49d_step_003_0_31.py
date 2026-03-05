import cadquery as cq

# Parametric dimensions
wall_t = 2.0
base_t = 3.0
tray_h = 12.0

# Column widths and row heights for the grid layout
w_cols = [30.0, 30.0, 45.0, 45.0]
h_rows = [25.0, 25.0, 50.0]

# Dimple/bump parameters
bump_rad = 1.8
bump_height = 0.8
bump_pitch = 4.0

# Calculated inner and outer dimensions
inner_w = sum(w_cols) + (len(w_cols) - 1) * wall_t
inner_d = sum(h_rows) + (len(h_rows) - 1) * wall_t

outer_w = inner_w + 2 * wall_t
outer_d = inner_d + 2 * wall_t

# 1. Base Tray Block
base_block = cq.Workplane("XY").box(outer_w, outer_d, tray_h)

# 2. Voids Definition
start_x = -inner_w / 2
start_y = -inner_d / 2

def get_void(col_idx, row_idx, colspan=1, rowspan=1):
    x_min = start_x + sum(w_cols[:col_idx]) + col_idx * wall_t
    w = sum(w_cols[col_idx:col_idx+colspan]) + (colspan - 1) * wall_t
    y_min = start_y + sum(h_rows[:row_idx]) + row_idx * wall_t
    h = sum(h_rows[row_idx:row_idx+rowspan]) + (rowspan - 1) * wall_t
    return x_min + w / 2, y_min + h / 2, w, h

# List of compartments: (col_start, row_start, col_span, row_span)
void_defs = [
    (0, 0, 1, 1),  # Bottom 1 (left)
    (1, 0, 1, 1),  # Bottom 2
    (2, 0, 1, 1),  # Bottom 3
    (3, 0, 1, 1),  # Bottom 4 (right)
    (0, 1, 1, 1),  # Middle Left
    (1, 1, 2, 1),  # Middle Center
    (3, 1, 1, 1),  # Middle Right
    (0, 2, 2, 1),  # Top Left
    (2, 2, 2, 1)   # Top Right
]

# 3. Cut Voids
cut_depth = tray_h - base_t
wp = base_block.faces(">Z").workplane()
for v in void_defs:
    cx, cy, w, h = get_void(*v)
    wp = wp.center(cx, cy).rect(w, h).center(-cx, -cy)
result = wp.cutBlind(-cut_depth)

# 4. Create Dimple Pattern on Floor
floor_z = -tray_h / 2 + base_t

# Determine sphere center to form domes of 'bump_height' above the floor
sphere_center_z = floor_z - bump_rad + bump_height

num_x = int(inner_w / bump_pitch)
num_y = int(inner_d / bump_pitch)
grid_start_x = - (num_x - 1) * bump_pitch / 2
grid_start_y = - (num_y - 1) * bump_pitch / 2

bump_pts = []
for i in range(num_x):
    for j in range(num_y):
        bump_pts.append((grid_start_x + i * bump_pitch, grid_start_y + j * bump_pitch))

bumps = (
    cq.Workplane("XY")
    .workplane(offset=sphere_center_z)
    .pushPoints(bump_pts)
    .sphere(bump_rad)
)

# 5. Union bumps with the tray (bumps inside walls will be cleanly absorbed)
result = result.union(bumps)