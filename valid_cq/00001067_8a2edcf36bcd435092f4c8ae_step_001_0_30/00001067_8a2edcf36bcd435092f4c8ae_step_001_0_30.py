import cadquery as cq

# Parametric dimensions
plate_thickness = 3.0
total_height = 80.0
max_width = 160.0      # Width at the bottom wing tips
top_width = 100.0      # Width at the top edge
cutout_width = 50.0
cutout_depth = 25.0    # Depth of the rectangular cutout from the bottom
wing_tip_flat = 12.0   # Height of the vertical flat edge at the wing tips

# Hole parameters
large_hole_diam = 8.0
large_hole_spacing = 24.0
small_hole_diam = 3.5
small_hole_top_spacing = 70.0 # Distance between top small holes
small_hole_bot_spacing = 44.0 # Distance between bottom small holes
small_hole_top_y_offset = 20.0
small_hole_bot_y_offset = -8.0

# Derived coordinates
# Origin (0,0) is placed roughly at the center of mass (between large holes)
y_top = 35.0
y_bottom = y_top - total_height        # -45.0
y_cutout = y_bottom + cutout_depth     # -20.0
y_wing_shoulder = y_bottom + wing_tip_flat 

x_top = top_width / 2.0
x_bot = max_width / 2.0
x_cutout = cutout_width / 2.0

# Define vertices for the outer profile (clockwise)
pts = [
    (0, y_top),                    # Top center start
    (x_top, y_top),                # Top right corner
    (x_bot, y_wing_shoulder),      # Angled side down to wing tip shoulder
    (x_bot, y_bottom),             # Vertical wing tip
    (x_cutout, y_bottom),          # Bottom right inner corner
    (x_cutout, y_cutout),          # Cutout vertical right
    (-x_cutout, y_cutout),         # Cutout vertical left
    (-x_cutout, y_bottom),         # Bottom left inner corner
    (-x_bot, y_bottom),            # Vertical wing tip left
    (-x_bot, y_wing_shoulder),     # Angled side up
    (-x_top, y_top)                # Top left corner
]

# Generate the model
result = (
    cq.Workplane("XY")
    .moveTo(pts[0][0], pts[0][1])
    .polyline(pts[1:])
    .close()
    .extrude(plate_thickness)
    .faces(">Z")
    .workplane()
    # Create the two large central holes
    .pushPoints([(large_hole_spacing/2, 0), (-large_hole_spacing/2, 0)])
    .hole(large_hole_diam)
    # Create the top pair of small holes
    .pushPoints([
        (small_hole_top_spacing/2, small_hole_top_y_offset), 
        (-small_hole_top_spacing/2, small_hole_top_y_offset)
    ])
    .hole(small_hole_diam)
    # Create the bottom pair of small holes
    .pushPoints([
        (small_hole_bot_spacing/2, small_hole_bot_y_offset), 
        (-small_hole_bot_spacing/2, small_hole_bot_y_offset)
    ])
    .hole(small_hole_diam)
)