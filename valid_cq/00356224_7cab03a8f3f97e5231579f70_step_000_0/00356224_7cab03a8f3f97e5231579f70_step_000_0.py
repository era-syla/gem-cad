import cadquery as cq

# --- Parametric Dimensions ---
length = 150.0
width = 50.0
height = 12.0
wall_thickness = 2.0
chamfer_size = 6.0

# Window cutout dimensions
window_length = 95.0
window_width = 28.0

# Detail feature dimensions and positions
detail_center_x = -58.0  # Center of the left detailing area relative to origin
button_radius = 4.0
button_depth = 1.5
slot_w = 1.2
slot_l = 5.0
slot_spacing = 2.5
tab_width = 6.0
tab_depth = 3.0

# --- Geometry Construction ---

# 1. Base Body
# Create the main rectangular block centered at the origin
result = cq.Workplane("XY").box(length, width, height)

# 2. Beveled Profile
# Apply a chamfer to the top edges to create the angled bezel shape
result = result.faces(">Z").edges().chamfer(chamfer_size)

# 3. Hollow Core
# Shell the object from the bottom face to create the tray-like structure
result = result.faces("<Z").shell(-wall_thickness)

# 4. Central Window
# Cut the large rectangular opening through the top face
result = result.faces(">Z").workplane().rect(window_length, window_width).cutThruAll()

# 5. Surface Details (Left Side)
# 5a. Circular Recess
# Positioned on the flat top surface to the left of the window
result = result.faces(">Z").workplane().center(detail_center_x, 0) \
    .circle(button_radius).cutBlind(-button_depth)

# 5b. Vents/Slots
# Three small slots positioned slightly towards the center from the button
# rarray is used to create the linear pattern (3 columns, 1 row)
result = result.faces(">Z").workplane().center(detail_center_x + 12, 0) \
    .rarray(slot_spacing, 1, 3, 1) \
    .rect(slot_w, slot_l) \
    .cutBlind(-button_depth)

# 6. Internal Mounting Tab
# A small tab protruding downwards from the internal frame edge
# Calculate the Z-level of the underside of the top face
underside_z = (height / 2.0) - wall_thickness

# Create workplane at the underside level
# Positioned offset in X and on the edge of the window in Y
# Extrude downwards to create the tab
result = result.workplane(offset=underside_z).center(30, window_width/2 + wall_thickness/2) \
    .rect(tab_width, wall_thickness).extrude(-tab_depth)
