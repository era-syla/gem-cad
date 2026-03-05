import cadquery as cq

# --- Parameters ---

# Back plate dimensions
back_length = 200.0
back_height = 30.0
back_thickness = 5.0

# Arm dimensions
arm_length = 100.0  # Length extending from the back plate
arm_width = 5.0     # Width of the arm (same as back_thickness usually looks good)
arm_height = 8.0    # Height of the arm profile

# Spacing
num_arms = 5
# Calculate spacing to distribute arms evenly. 
# Total span is back_length. Arms are centered.
# Spacing between arm centers.
spacing = (back_length - (2 * arm_width)) / (num_arms - 1) 
# Alternatively, fixed spacing:
# spacing = 40.0 

# Notch details (at the end of the arms)
notch_depth = 2.0
notch_width = 2.0
notch_offset_from_end = 2.0 # Distance from the tip to the start of the notch

# --- Modeling ---

# 1. Create the Back Plate
# Centered on X and Y for symmetry
back_plate = cq.Workplane("XY").box(back_length, back_thickness, back_height)

# 2. Define a single Arm
# We will create one arm and then replicate it.
# The arm attaches to the front face of the back plate.

# We build the arm starting at the origin, extending in Y.
arm = (
    cq.Workplane("XY")
    .box(arm_width, arm_length, arm_height)
    # Move arm so its back face aligns with the origin
    .translate((0, arm_length / 2, 0))
)

# 3. Add the Notch to the Arm
# We cut a small slot near the end of the arm on the top face.
# Top face is Z = arm_height/2
notch_center_y = arm_length - notch_offset_from_end - (notch_width/2)

cutter = (
    cq.Workplane("XY")
    .box(arm_width, notch_width, notch_depth)
    .translate((0, notch_center_y, arm_height/2))
)

arm_with_notch = arm.cut(cutter)

# 4. Position and Pattern the Arms

# We need to position the arms relative to the back plate.
# The back plate is at (0,0,0) (center).
# Its front face is at Y = -back_thickness/2 (since thickness is Y dimension).
# Wait, let's re-orient. 
# If Back Plate is box(L, T, H), let's assume L is X, T is Y, H is Z.
# Back plate center is (0,0,0). Front face is Y = back_thickness/2.
# Arms extend in positive Y direction from that face.
# Arms need to be flush with the bottom of the back plate? 
# Looking at the image, the arms seem aligned with the bottom edge of the back plate.

back_plate_bottom_z = -back_height / 2
arm_bottom_z = -arm_height / 2
z_shift = back_plate_bottom_z - arm_bottom_z 

# The arms actually look like they are attached to the *bottom* of the back plate 
# or the lower part of the face. In the image, the top of the arm is below the top 
# of the back plate. Let's align them flush at the bottom.

# Start position for the first arm (leftmost)
start_x = -(back_length / 2) + (arm_width / 2) # Just inside the edge? 
# The image shows the outer arms are flush with the ends of the back plate.
start_x = -(back_length / 2) + (arm_width / 2)

# Calculate positions for all arms
arm_positions = []
for i in range(num_arms):
    # If we want exact flush ends, we recalculate spacing based on centers
    # Span between center of first and center of last arm
    center_span = back_length - arm_width 
    step = center_span / (num_arms - 1)
    
    pos_x = -(center_span / 2) + (i * step)
    
    # Y position: The arm starts at y=0 relative to its local origin, 
    # but we need it to start at the face of the backplate.
    # Backplate Y extent is -thickness/2 to +thickness/2.
    # We want arm to start at +thickness/2.
    pos_y = back_thickness / 2
    
    # Z position: Align bottoms
    # Backplate bottom is at -back_height/2
    # Arm bottom is at -arm_height/2 relative to its center.
    # We want (Z_arm_center - arm_height/2) = (Z_back_center - back_height/2)
    pos_z = (-back_height / 2) + (arm_height / 2)
    
    arm_positions.append((pos_x, pos_y, pos_z))

# 5. Combine Everything

result = back_plate

for pos in arm_positions:
    # Translate the standard arm to the position
    current_arm = arm_with_notch.translate(pos)
    result = result.union(current_arm)

# Export or Display
# show_object(result)