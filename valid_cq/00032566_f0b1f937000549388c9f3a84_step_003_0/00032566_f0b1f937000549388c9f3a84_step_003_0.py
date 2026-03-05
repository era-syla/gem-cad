import cadquery as cq

# --- Parametric Dimensions ---
length = 220.0          # Total length of the part
bar_height = 25.0       # Height of the main horizontal bar
thickness = 8.0         # Thickness of the plate

# Left Handle Geometry
handle_height = 50.0
handle_width = 45.0     # Width of the flat bottom section of the handle
handle_slope_w = 20.0   # Horizontal width of the slope transition

# Middle Tooth Geometry
tooth_pos_x = 130.0     # X position of the tooth center (from origin)
tooth_depth = 15.0      # How far down the tooth protrudes
tooth_top_w = 35.0      # Width of the tooth at the bar connection
tooth_bot_w = 15.0      # Width of the flat bottom of the tooth

# Right Tip Geometry
tip_height = 15.0       # Height of the vertical face at the right tip
chamfer_w = 10.0        # Horizontal width of the bottom chamfer

# Cutout Dimensions
handle_wall = 10.0      # Wall thickness around the handle cutout
mid_slot_w = 15.0       # Width of the middle rectangular slot
mid_slot_h = 8.0        # Height of the middle rectangular slot
tip_slot_h = 10.0       # Height (length) of the vertical slot at the tip
tip_slot_w = 3.5        # Width of the vertical slot at the tip

# --- Geometry Construction ---

# Define profile points starting from Top-Left (0,0) and going Clockwise
# Note: Since Y is up in 2D sketching, negative Y values go down.
pts = []
pts.append((0, 0))                                      # Top Left
pts.append((length, 0))                                 # Top Right
pts.append((length, -tip_height))                       # Right Tip Bottom
pts.append((length - chamfer_w, -bar_height))           # End of Right Chamfer

# Middle section (Right to Left along bottom)
tooth_start_right = tooth_pos_x + tooth_top_w / 2
tooth_start_left = tooth_pos_x - tooth_top_w / 2
tooth_bot_right = tooth_pos_x + tooth_bot_w / 2
tooth_bot_left = tooth_pos_x - tooth_bot_w / 2

pts.append((tooth_start_right, -bar_height))            # Start of Tooth (Right)
pts.append((tooth_bot_right, -bar_height - tooth_depth))# Tooth Bottom Right
pts.append((tooth_bot_left, -bar_height - tooth_depth)) # Tooth Bottom Left
pts.append((tooth_start_left, -bar_height))             # End of Tooth (Left)

# Handle section transition
slope_start_x = handle_width + handle_slope_w
pts.append((slope_start_x, -bar_height))                # Start of Handle Slope
pts.append((handle_width, -handle_height))              # Bottom of Handle Slope
pts.append((0, -handle_height))                         # Bottom Left Corner

# 1. Create Base Solid
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# 2. Create Left Handle Cutout
# Calculated to follow the outer contour offset by 'handle_wall'
cutout_pts = [
    (handle_wall, -handle_wall),                                             # Top Left
    (slope_start_x - handle_wall * 0.8, -handle_wall),                       # Top Right
    (handle_width - handle_wall * 0.5, -handle_height + handle_wall),        # Bottom Right (sloped)
    (handle_wall, -handle_height + handle_wall)                              # Bottom Left
]

result = (
    result.faces(">Z")
    .workplane()
    .polyline(cutout_pts)
    .close()
    .cutBlind(-thickness)
)

# 3. Create Middle Rectangular Slot
# Centered above the tooth
result = (
    result.faces(">Z")
    .workplane()
    .center(tooth_pos_x, -bar_height / 2)
    .rect(mid_slot_w, mid_slot_h)
    .cutBlind(-thickness)
)

# 4. Create Right Vertical Slot
# Positioned near the tip
tip_slot_x = length - 10.0
tip_slot_y = -tip_height / 2 - 2.0  # Slightly adjusted to be visually centered

result = (
    result.faces(">Z")
    .workplane()
    .center(tip_slot_x, tip_slot_y)
    .slot2D(tip_slot_h, tip_slot_w, 90) # Vertical slot
    .cutBlind(-thickness)
)