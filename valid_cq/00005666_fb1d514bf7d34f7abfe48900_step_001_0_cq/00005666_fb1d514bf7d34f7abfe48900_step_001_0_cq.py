import cadquery as cq

# --- Parametric Dimensions ---
# Overall length of the extrusion
length = 50.0

# Dimensions for the main rectangular block (right side)
main_block_width = 20.0
main_block_height = 20.0

# Dimensions for the stepped features (left side)
step_count = 3
step_width = 4.0
step_height = 2.0  # Height of each individual step riser

# The "leg" on the far left
left_leg_width = 4.0
left_leg_total_height = 15.0  # Total height from top of first step to bottom of leg

# Angle/Position for the slanted cutout
cutout_top_offset = 5.0 # How far down from the top block surface the cutout starts
leg_bottom_y = -10.0 # Y position of the bottom of the legs relative to the main block bottom

# --- Geometric Construction ---

# Calculate derived dimensions for sketching
# We will sketch on the XZ plane and extrude along Y (or Z, depending on orientation preference, let's stick to standard XY sketch, extrude Z)
# Let's visualize the profile in 2D (XY plane) and extrude in Z for length.

# Starting point: Bottom right corner of the main block
# Coordinate system: (0,0) is bottom-right corner of the profile

pts = []

# 1. Right vertical line (main block)
pts.append((0, 0)) 
pts.append((0, main_block_height))

# 2. Top horizontal line (main block)
pts.append((-main_block_width, main_block_height))

# 3. Steps going down and left
current_x = -main_block_width
current_y = main_block_height

for i in range(step_count):
    # Step down
    current_y -= step_height
    pts.append((current_x, current_y))
    # Step left
    current_x -= step_width
    pts.append((current_x, current_y))

# 4. The vertical outer edge of the left leg
# The leg goes down to a certain depth. 
# Let's say the leg bottom is aligned with the main block bottom for simplicity, 
# or slightly different based on the image. The image shows the leg going down quite a bit.
# Let's define the leg bottom relative to the top of the last step.
leg_bottom_y = current_y - left_leg_total_height
pts.append((current_x, leg_bottom_y))

# 5. The bottom thickness of the left leg
pts.append((current_x + left_leg_width, leg_bottom_y))

# 6. The angled undercut
# We need to go from the inner bottom of the left leg to the inner bottom of the main block.
# Looking at the image, there is a distinct angled cutout.
# Let's define the "ceiling" of the cutout. It seems to start up high near the steps.
# Let's pick a point for the apex of the cutout.
cutout_apex_x = -main_block_width
cutout_apex_y = main_block_height - (step_count * step_height) - 2.0 # Slightly below the steps

# The image shows a simple bridge-like structure.
# Let's trace back from the left leg bottom up to the "bridge" underside, then down to main leg.

# Inner wall of left leg
underside_leg_height = 8.0 # How far up the cutout goes
pts.append((current_x + left_leg_width, leg_bottom_y + underside_leg_height))

# Connect to the main block. The main block seems to have a slanted inner wall.
# Let's look at the bottom of the main block.
main_block_bottom_width = main_block_width * 0.7 # Tapered slightly? Or straight?
# Image shows the main block is mostly rectangular but the cutout creates a slant.
# Let's define the bottom-left point of the main block.
main_block_bottom_left_x = -main_block_width
main_block_bottom_left_y = 0.0

# It looks like the cutout creates a single angled face from the left leg to the main block.
# Let's revise point 6.
# From (current_x + left_leg_width, leg_bottom_y) -> angled line -> (-main_block_width, 0)
# This creates the triangular void.

# Actually, the image shows a flat-ish area under the steps.
# Let's try:
# Up from left leg bottom
cutout_left_inner_x = current_x + left_leg_width
cutout_left_inner_y = leg_bottom_y + 6.0 # Arbitrary height for the vertical part of the cutout

pts.append((cutout_left_inner_x, cutout_left_inner_y))

# Angled line to the bottom-left corner of the main block geometry
# The main block geometry starts at x = -main_block_width. 
# The bottom of the main block is at y=0.
# However, the main block looks deeper than the leg in the image? No, they look roughly coplanar at the bottom.
# Let's assume the main block goes down to y = leg_bottom_y as well to act as a foot?
# The image shows the right block is massive. Let's assume the right block bottom is at y = leg_bottom_y.
# Wait, looking at the very first point (0,0), let's shift that.

# --- Redefining Geometry strategy based on clearer look ---
# The shape is an extrusion.
# Let's define the profile on the YZ plane (where Z is up, Y is width) and extrude X.
# 
# Origin: Bottom right corner of the solid.
# Profile points:
# 1. (0, 0) -> Bottom Right
# 2. (0, 25) -> Top Right (Height)
# 3. (-20, 25) -> Top Left of main block
# 4. Stairs:
#    - Down 2, Left 3
#    - Down 2, Left 3
#    - Down 2, Left 3
# 5. Outer Left Wall: Down to bottom.
# 6. Bottom Left: Across thickness.
# 7. Inner cutout: Up and angled right to meet the main block.

height = 25.0
width_right_block = 20.0
step_dy = 2.0
step_dx = 3.0
num_steps = 3
leg_thickness = 4.0
# The bottom of the left leg seems to be at the same level as the bottom of the right block.
# Let's assume Z=0 is the bottom.

# Start creating the profile
result = cq.Workplane("XY")

def create_profile():
    # Helper variables
    h = 30.0 # Total Height
    w_main = 25.0 # Width of the main block
    
    # Stairs
    s_run = 3.0
    s_rise = 1.5
    n_stairs = 3
    
    # Left Leg
    leg_w = 4.0
    
    # Calculation of total width
    total_width = w_main + (n_stairs * s_run) + leg_w
    
    # Start at bottom right corner (local 0,0)
    pts = []
    pts.append((0, 0)) # Bottom Right
    pts.append((0, h)) # Top Right
    pts.append((-w_main, h)) # Top Left of main block
    
    curr_x = -w_main
    curr_y = h
    
    # Stairs
    for _ in range(n_stairs):
        curr_y -= s_rise # Down
        pts.append((curr_x, curr_y))
        curr_x -= s_run # Left
        pts.append((curr_x, curr_y))
        
    # Final lip/edge of the last step top is the top of the leg
    
    # Outer left wall
    pts.append((curr_x, 0)) # Bottom Left (assuming flat bottom alignment)
    
    # Bottom thickness of left leg
    pts.append((curr_x + leg_thickness, 0))
    
    # The Cutout / Underside
    # Go Up vertical inside leg
    cutout_h = 10.0
    pts.append((curr_x + leg_thickness, cutout_h))
    
    # Angled line to the inner wall of the main block
    # The inner wall of the main block is at x = -w_main
    # But where does it hit? Maybe slightly below the stairs?
    # Or simply connects to the bottom corner (-w_main, 0)?
    # Looking at the image, there is a sharp corner under the steps.
    # Let's connect to (-w_main, cutout_h + some_rise) or just straight to (-w_main, 0)
    # The image shows a triangular void.
    # Let's connect to (-w_main, 0).
    pts.append((-w_main, 0))
    
    pts.append((0,0)) # Close loop
    
    return pts

# Generate profile points
profile_points = create_profile()

# Create the solid
result = (
    cq.Workplane("YZ")
    .polyline(profile_points)
    .close()
    .extrude(60) # Extrude along X axis
)