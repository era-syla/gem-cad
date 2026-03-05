import cadquery as cq

# --- Parameters ---
total_length = 120.0
main_width = 30.0
thickness = 10.0
tab_length = 15.0
tab_width = 15.0

# Cutout parameters
triangle_gap = 5.0        # Gap between the tips of the triangles
triangle_margin = 8.0     # Margin from the end of the main body to the triangle base
triangle_base_width = 18.0

# --- Calculations ---
main_body_length = total_length - (2 * tab_length)
x_main = main_body_length / 2.0
x_total = total_length / 2.0
y_main = main_width / 2.0
y_tab = tab_width / 2.0

# --- Geometry Creation ---

# Define the outer profile points (starting top-right of main body, going clockwise)
profile_pts = [
    (x_main, y_main),       # Top-right corner main body
    (x_main, y_tab),        # Step down
    (x_total, y_tab),       # Tab top-right
    (x_total, -y_tab),      # Tab bottom-right
    (x_main, -y_tab),       # Step back
    (x_main, -y_main),      # Bottom-right corner main body
    (-x_main, -y_main),     # Bottom-left corner main body
    (-x_main, -y_tab),      # Step down
    (-x_total, -y_tab),     # Tab bottom-left
    (-x_total, y_tab),      # Tab top-left
    (-x_main, y_tab),       # Step back
    (-x_main, y_main),      # Top-left corner main body
    (x_main, y_main)        # Close loop
]

# Extrude the main body
body = cq.Workplane("XY").polyline(profile_pts).close().extrude(thickness)

# Define triangular cutouts
# Right triangle (pointing inwards/left)
x_tip_r = triangle_gap / 2.0
x_base_r = x_main - triangle_margin
pts_tri_right = [
    (x_tip_r, 0),
    (x_base_r, triangle_base_width / 2.0),
    (x_base_r, -triangle_base_width / 2.0)
]

# Left triangle (pointing inwards/right)
x_tip_l = -triangle_gap / 2.0
x_base_l = -x_main + triangle_margin
pts_tri_left = [
    (x_tip_l, 0),
    (x_base_l, triangle_base_width / 2.0),
    (x_base_l, -triangle_base_width / 2.0)
]

# Apply cuts to the body
result = (
    body.faces(">Z").workplane()
    .polyline(pts_tri_right).close()
    .polyline(pts_tri_left).close()
    .cutBlind(-thickness)
)