import cadquery as cq

# --- Parameters ---
length = 150.0        # Total length of the part
height = 25.0         # Height of the extrusion
thickness = 3.0       # Wall thickness
depth = 18.0          # Outer depth of the hooks and tabs

hook_return = 12.0    # Length of the C-shape return at the ends
tab_width = 12.0      # Width of the intermediate U-shaped tabs
tab_spacing = 60.0    # Distance between the centers of the tabs
fillet_radius = 2.0   # Radius for corner fillets

# --- Geometry Calculation ---

# Calculate centerline coordinates
# We define the path along the center of the wall to use offset2D symmetrically
# Z-axis is height, XY plane is the profile

# Y-coordinates for the centerline
# Back wall centerline is at 0, Front features extend to negative Y
cl_y_back = 0.0
cl_y_front = -(depth - thickness) 

# X-coordinates for the centerline path (Left to Right)
# Adjusting for thickness to approximate outer dimensions
x_outer = length / 2.0 - thickness / 2.0
x_hook_tip = x_outer - hook_return

# Tab positions relative to center
x_tab_pos = tab_spacing / 2.0
x_tab_half_w = tab_width / 2.0

# Define points for the polyline spine (Left -> Right)
points = [
    # Left End Hook
    (-x_hook_tip, cl_y_front),
    (-x_outer, cl_y_front),
    (-x_outer, cl_y_back),
    
    # Left Tab
    (-(x_tab_pos + x_tab_half_w), cl_y_back),
    (-(x_tab_pos + x_tab_half_w), cl_y_front),
    (-(x_tab_pos - x_tab_half_w), cl_y_front),
    (-(x_tab_pos - x_tab_half_w), cl_y_back),
    
    # Right Tab
    ((x_tab_pos - x_tab_half_w), cl_y_back),
    ((x_tab_pos - x_tab_half_w), cl_y_front),
    ((x_tab_pos + x_tab_half_w), cl_y_front),
    ((x_tab_pos + x_tab_half_w), cl_y_back),
    
    # Right End Hook
    (x_outer, cl_y_back),
    (x_outer, cl_y_front),
    (x_hook_tip, cl_y_front)
]

# --- Model Generation ---

result = (
    cq.Workplane("XY")
    .polyline(points)
    # Create the wall by offsetting the centerline in both directions
    # kind="intersection" creates sharp corners that we will fillet later
    .offset2D(thickness / 2.0, kind="intersection")
    .extrude(height)
    # Apply fillets to all vertical edges to round the corners
    .edges("|Z")
    .fillet(fillet_radius)
)