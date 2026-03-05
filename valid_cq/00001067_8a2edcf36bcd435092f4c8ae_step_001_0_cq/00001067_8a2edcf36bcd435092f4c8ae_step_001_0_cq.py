import cadquery as cq

# --- Parameters ---
plate_thickness = 3.0

# Overall dimensions approximation based on visual aspect ratio
total_width = 180.0
total_depth = 120.0  # From back edge to tips of the wings

# Central rectangular section
center_width = 80.0
center_depth = 80.0

# Wings (the angled side pieces)
wing_width = (total_width - center_width) / 2
wing_start_depth = 30.0 # How far down the side the wing starts
wing_tip_width = 20.0   # The flat part at the tip of the wing

# Cutout at the front
cutout_width = 50.0
cutout_depth = 30.0

# Holes
large_hole_diam = 12.0
large_hole_spacing = 30.0

small_hole_diam = 4.0
# Coordinates for small holes relative to center
# Top row (back)
small_hole_back_y = 25.0
small_hole_back_x = 35.0
# Middle row
small_hole_mid_y = 5.0
small_hole_mid_x = 25.0 # Just a guess based on asymmetry
# Front row
small_hole_front_y = -20.0
small_hole_front_x = 20.0

# --- Modeling ---

# We will define the shape by points on the XY plane and extrude
# Let's assume the origin (0,0) is the center of the main rectangular body

# Calculating vertices for a polygon
# Order: Start top-left corner of center, go counter-clockwise
pts = [
    # Top edge
    (-center_width/2, center_depth/2),
    (center_width/2, center_depth/2),
    
    # Right side down to wing start
    (center_width/2, center_depth/2 - wing_start_depth),
    
    # Right wing outer edge
    (total_width/2, center_depth/2 - wing_start_depth - 15), # angled part out
    (total_width/2, -center_depth/2 + 10), # straight side
    
    # Right wing tip
    (total_width/2 - 10, -center_depth/2), # angled tip
    
    # Right inner cutout
    (cutout_width/2, -center_depth/2),
    (cutout_width/2, -center_depth/2 + cutout_depth),
    (-cutout_width/2, -center_depth/2 + cutout_depth),
    (-cutout_width/2, -center_depth/2),
    
    # Left wing tip
    (-(total_width/2 - 10), -center_depth/2),
    
    # Left wing outer edge
    (-total_width/2, -center_depth/2 + 10),
    (-total_width/2, center_depth/2 - wing_start_depth - 15),
    
    # Left side up to start
    (-center_width/2, center_depth/2 - wing_start_depth),
]

# Let's refine the shape approach. It looks like a T-shape or Pi-shape.
# It's easier to sketch it.

# Main body rectangle
main_body = cq.Workplane("XY").rect(center_width, center_depth)

# The wings
# Left Wing
left_wing_pts = [
    (-center_width/2, 0),
    (-total_width/2, -20), # angled out
    (-total_width/2, -center_depth/2 + 10),
    (-total_width/2 + 15, -center_depth/2),
    (-center_width/2, -center_depth/2),
]
# Right Wing
right_wing_pts = [
    (center_width/2, 0),
    (total_width/2, -20),
    (total_width/2, -center_depth/2 + 10),
    (total_width/2 - 15, -center_depth/2),
    (center_width/2, -center_depth/2),
]

# Actually, let's just trace the outline relative to a center point between the two large holes.
# Let's say origin (0,0) is exactly between the two large holes.

# Key dimensions for points
half_w_inner = 40.0   # Half width of the central block
half_w_outer = 90.0   # Half width to the wing tip
y_top = 40.0          # Top edge
y_bot_cutout = -10.0  # Bottom of the central cutout
y_bot_wing = -40.0    # Bottom of the wing tips
cutout_half_w = 25.0  # Half width of the bottom cutout

# Define points counter-clockwise starting from top-right
points = [
    (half_w_inner, y_top),          # Top Right Corner
    (-half_w_inner, y_top),         # Top Left Corner
    (-half_w_inner, 0),             # Left side, start of wing flare
    (-half_w_outer, -15),           # Left Wing flare out
    (-half_w_outer, y_bot_wing + 10), # Left Wing vertical edge
    (-half_w_outer + 15, y_bot_wing), # Left Wing angled tip
    (-cutout_half_w, y_bot_wing),   # Left Wing inner bottom
    (-cutout_half_w, y_bot_cutout), # Cutout vertical up
    (cutout_half_w, y_bot_cutout),  # Cutout horizontal
    (cutout_half_w, y_bot_wing),    # Cutout vertical down
    (half_w_outer - 15, y_bot_wing),# Right Wing angled tip
    (half_w_outer, y_bot_wing + 10),# Right Wing vertical edge
    (half_w_outer, -15),            # Right Wing flare out
    (half_w_inner, 0)               # Right side, start of wing flare
]

# Create base plate
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(plate_thickness)
)

# Add Large Holes (Central pair)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-large_hole_spacing/2, 0), (large_hole_spacing/2, 0)])
    .hole(large_hole_diam)
)

# Add Small Holes
# There appear to be 4 small holes in a somewhat symmetric pattern, plus maybe one offset one.
# Looking closely at the image:
# 1. Top left (near corner)
# 2. Top right (near corner) - WAIT, image shows top right hole, but top left is obscured or missing?
#    Let's assume symmetry on the back corners.
# 3. Near the left large hole
# 4. Near the right large hole (slightly lower)

# Let's define specific coordinates based on visual estimation relative to (0,0) center
small_hole_coords = [
    (-half_w_inner + 10, y_top - 10), # Top Left
    (half_w_inner - 10, y_top - 10),  # Top Right (visible)
    (-15, 15), # Near left center
    (15, -15)  # Near right center (lower)
]

# Looking closer at image, there is a hole at the bottom center of the main block too?
# Let's stick to the 4 clearly visible ones and maintain symmetry where plausible.
# The image actually shows:
# - One near top-left of the center block
# - One near the middle-left of the center block
# - One near bottom-center
# - One on the right wing? No.

# Revised small hole positions based on the specific image:
# 1. Back Left
# 2. Middle Left (near the large hole)
# 3. Front Center (below the large holes)
# 4. Far Right (on the wing extension)

pts_small_holes = [
    (-20, 25),   # Back Left-ish
    (-30, 5),    # Mid Left
    (0, -20),    # Bottom Center
    (70, -25)    # Right Wing hole
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(pts_small_holes)
    .hole(small_hole_diam)
)