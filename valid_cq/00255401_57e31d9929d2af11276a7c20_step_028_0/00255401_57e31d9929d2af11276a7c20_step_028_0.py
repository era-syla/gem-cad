import cadquery as cq

# Parametric Dimensions
total_length = 100.0     # Overall length of the part
main_width = 30.0        # Width of the central main body section
thickness = 10.0         # Thickness of the plate
tab_length = 10.0        # Length of the connection tabs at the ends
tab_width = 15.0         # Width of the connection tabs

# Cutout Parameters
wall_thickness = 4.0     # Wall thickness between cutout and outer edge
center_gap = 6.0         # Solid material bridging the two cutouts in the center

# Derived Dimensions
main_length = total_length - 2 * tab_length
half_main_len = main_length / 2.0
half_main_width = main_width / 2.0
half_tab_width = tab_width / 2.0
half_total_len = total_length / 2.0

# 1. Create the base profile
# Define points for the outer contour (counter-clockwise)
pts = [
    (half_main_len, half_main_width),       # Top-Right of main body
    (half_main_len, half_tab_width),        # Step down to tab
    (half_total_len, half_tab_width),       # Top-Right of tab
    (half_total_len, -half_tab_width),      # Bottom-Right of tab
    (half_main_len, -half_tab_width),       # Step back to main body
    (half_main_len, -half_main_width),      # Bottom-Right of main body
    (-half_main_len, -half_main_width),     # Bottom-Left of main body
    (-half_main_len, -half_tab_width),      # Step to left tab
    (-half_total_len, -half_tab_width),     # Bottom-Left of tab
    (-half_total_len, half_tab_width),      # Top-Left of tab
    (-half_main_len, half_tab_width),       # Step back to main body
    (-half_main_len, half_main_width)       # Top-Left of main body
]

# Create the solid base block
base = cq.Workplane("XY").polyline(pts).close().extrude(thickness)

# 2. Define geometry for triangular cutouts
# Calculate boundaries for the triangles
tri_max_x = half_main_len - wall_thickness
tri_min_x = center_gap / 2.0
tri_half_y = half_main_width - wall_thickness

# Define vertices for the right triangle (pointing left)
r_p1 = (tri_min_x, 0)                 # Tip
r_p2 = (tri_max_x, tri_half_y)        # Top base corner
r_p3 = (tri_max_x, -tri_half_y)       # Bottom base corner

# Define vertices for the left triangle (pointing right)
l_p1 = (-tri_min_x, 0)                # Tip
l_p2 = (-tri_max_x, tri_half_y)       # Top base corner
l_p3 = (-tri_max_x, -tri_half_y)      # Bottom base corner

# 3. Apply the cuts
result = (
    base
    .faces(">Z")
    .workplane()
    # Draw Right Triangle
    .polyline([r_p1, r_p2, r_p3]).close()
    # Draw Left Triangle
    .polyline([l_p1, l_p3, l_p2]).close()
    .cutThruAll()
)