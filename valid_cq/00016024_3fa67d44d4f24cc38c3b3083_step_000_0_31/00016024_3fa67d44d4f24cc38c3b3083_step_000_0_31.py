import cadquery as cq

# --- Parameters ---
# Overall dimensions
W = 130.0
D = 100.0

# Left Wall / Main Body
w_left = 35.0
H_back = 90.0
h_front = 35.0

# Back Right Plate
d_back = 35.0
t_plate = 18.0

# Top Fin
t_fin = 8.0
h_fin = 45.0
flat_len = 15.0
y_fin_start = 25.0
h_fin_front = 5.0

# Notches on the bottom slanted edge
notch_width = 10.0
notch_depth = 8.0
notch_ys = [30.0, 60.0, 85.0]

# Holes
r_hole_main = 4.5
y_hole_main = 15.0
z_hole_main = -15.0

r_hole_fin = 3.5
offset_y_fin_hole = 8.0
offset_z_fin_hole = 8.0

# --- Geometry Generation ---

# 1. Left Wall Profile (in YZ plane)
def z_slant(y):
    """Calculate Z coordinate along the slanted bottom edge."""
    return -h_front + (y / D) * (h_front - H_back)

pts_left = [(0, 0), (D, 0), (D, -H_back)]

# Build the notched slanted edge from back to front
for y_notch in reversed(notch_ys):
    y_end = y_notch + notch_width / 2.0
    y_start = y_notch - notch_width / 2.0
    
    # Boundary checks
    if y_end > D: y_end = D
    if y_start < 0: y_start = 0
    
    z_end = z_slant(y_end)
    roof_z = z_end + notch_depth
    
    pts_left.append((y_end, z_end))         # Slant to notch start
    pts_left.append((y_end, roof_z))        # Vertical up
    pts_left.append((y_start, roof_z))      # Horizontal left
    pts_left.append((y_start, z_slant(y_start))) # Vertical down back to slant

pts_left.append((0, -h_front)) # Slant to the front tip

# Extrude the left wall
left_wall = (
    cq.Workplane("YZ")
    .polyline(pts_left).close()
    .extrude(w_left)
)

# 2. Back Plate
back_plate = (
    cq.Workplane("XY")
    .box(W - w_left, d_back, t_plate, centered=False)
    .translate((w_left, D - d_back, -t_plate))
)

# 3. Fin Profile
pts_fin = [
    (y_fin_start, 0),
    (D, 0),
    (D, h_fin),
    (D - flat_len, h_fin),
    (y_fin_start, h_fin_front)
]

fin = (
    cq.Workplane("YZ")
    .polyline(pts_fin).close()
    .extrude(t_fin)
    .translate((w_left - t_fin, 0, 0)) # Align right face of fin with inner face of left wall
)

# Combine the main bodies
result = left_wall.union(back_plate).union(fin)

# --- Features (Holes) ---

# Main body hole (front left)
result = result.cut(
    cq.Workplane("YZ")
    .center(y_hole_main, z_hole_main)
    .circle(r_hole_main)
    .extrude(w_left + 10)
    .translate((-5, 0, 0)) # Offset to ensure clean through-cut
)

# Fin hole (top back)
y_hole_fin = D - offset_y_fin_hole
z_hole_fin = h_fin - offset_z_fin_hole
result = result.cut(
    cq.Workplane("YZ")
    .center(y_hole_fin, z_hole_fin)
    .circle(r_hole_fin)
    .extrude(t_fin + 10)
    .translate((w_left - t_fin - 5, 0, 0))
)