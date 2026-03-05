import cadquery as cq

# --- Parametric Dimensions ---
case_width = 80.0
case_height = 160.0
case_thickness = 13.0
corner_radius = 10.0
top_chamfer_size = 3.0

# --- 1. Base Body Generation ---
# Create the main rectangular block centered at origin
base = cq.Workplane("XY").box(case_width, case_height, case_thickness)

# Round the vertical corners to create the basic phone shape
base = base.edges("|Z").fillet(corner_radius)

# Apply a chamfer to the top perimeter edges to match the rugged design
base = base.faces(">Z").edges().chamfer(top_chamfer_size)

# --- 2. Top Face Features ---

# Feature: Circular Camera/Sensor Bump (Top Center)
cam_y_pos = 45.0
cam_radius = 9.0
cam_height = 1.5

# Extrude the main cylinder
base = base.faces(">Z").workplane().center(0, cam_y_pos)\
    .circle(cam_radius).extrude(cam_height)

# Cut a slight recess/detail into the camera bump
base = base.faces(">Z").workplane().center(0, cam_y_pos)\
    .circle(cam_radius - 2.5).cutBlind(-0.5)

# Feature: Main Screen/Panel Recess (Center Body)
screen_w = 54.0
screen_h = 88.0
screen_y_pos = -8.0
screen_depth = 2.0

# Cut the main rectangular pocket
base = base.faces(">Z").workplane().center(0, screen_y_pos)\
    .rect(screen_w, screen_h).cutBlind(-screen_depth)

# Add a "shelf" or connector detail at the bottom of the screen pocket
base = base.faces(">Z").workplane().center(0, screen_y_pos - screen_h/2 + 6)\
    .rect(screen_w - 12, 8).cutBlind(-1.0)

# Feature: Secondary Rectangular Indentation (Bottom Right)
fp_w = 22.0
fp_h = 14.0
fp_x_pos = 18.0
fp_y_pos = -60.0

# Cut the recess
base = base.faces(">Z").workplane().center(fp_x_pos, fp_y_pos)\
    .rect(fp_w, fp_h).cutBlind(-screen_depth)

# Extrude a raised pad inside the recess (fingerprint sensor or label area)
base = base.faces(">Z").workplane().center(fp_x_pos, fp_y_pos)\
    .rect(fp_w - 4, fp_h - 4).extrude(0.8)

# --- 3. Top Edge Ports (+Y Face) ---
# Create ports for USB and Audio
# Note: On the >Y face, local X is global X, local Y is global Z (thickness)

base = base.faces(">Y").workplane().center(0, 0)

# Two rectangular slots (USB-C / Charging)
base = base.pushPoints([(-14, 0), (2, 0)])\
    .rect(8, 3.5).cutBlind(-10)

# Circular Audio Jack (Right side)
base = base.center(18, 0).circle(2.5).cutBlind(-10)

# --- 4. Side Interface (-X Face) ---
# Recessed control panel with buttons
# Note: On the <X face, local X aligns with global Y (length of phone)

side_recess_length = 55.0
side_recess_width = 5.0
side_features_center_y = 25.0  # Shifted towards the top half

# Cut the long channel for buttons
base = base.faces("<X").workplane().center(side_features_center_y, 0)\
    .rect(side_recess_length, side_recess_width).cutBlind(-1.0)

# Create 3 square buttons inside the channel
# We use offset to start the extrusion slightly below the main surface
btn_size = 4.0
base = base.faces("<X").workplane(offset=-0.2).center(side_features_center_y, 0)\
    .pushPoints([(-15, 0), (0, 0), (15, 0)])\
    .rect(btn_size, btn_size).extrude(1.5)

# Add small notches/details lower down the side
base = base.faces("<X").workplane().center(-45, 0)\
    .pushPoints([(-4, 0), (4, 0)])\
    .rect(1.5, 3.0).cutBlind(-1.0)

# --- Final Result ---
result = base