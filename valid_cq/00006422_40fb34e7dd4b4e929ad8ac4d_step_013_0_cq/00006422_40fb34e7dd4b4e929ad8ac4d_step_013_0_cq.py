import cadquery as cq
from math import degrees, atan2, sqrt

# --- Parametric Variables ---
# Units are arbitrary, assuming cm or similar scale
beam_thickness = 10.0
beam_width = 10.0
plank_thickness = 5.0
plank_width = 15.0

# Overall dimensions
height = 250.0
base_length = 100.0
top_arm_length = 180.0
width = 60.0  # Distance between the two main frames

# Angles and bracing
brace_angle = 45.0

# --- Helper Function for creating beams ---
def make_beam(length, w=beam_width, t=beam_thickness):
    return cq.Workplane("XY").box(length, w, t)

# --- Construction ---

# 1. Vertical Posts (The main uprights)
# Left and right vertical posts
post = make_beam(height, beam_width, beam_thickness).rotate((0,0,0), (0,1,0), 90)

left_post = post.translate((0, -width/2 + beam_width/2, height/2))
right_post = post.translate((0, width/2 - beam_width/2, height/2))

# 2. Top Horizontal Arms (Cantilevered beams)
# These sit on top or are mortised into the vertical posts. 
# Looking at image, they extend backwards and forwards, but mostly forwards.
arm = make_beam(top_arm_length, beam_width, beam_thickness)
# Shift so it starts flush with the back of the post and extends forward
arm_offset_x = (top_arm_length/2) - (beam_thickness/2) # Adjust alignment relative to post
left_arm = arm.translate((-arm_offset_x + 20, -width/2 + beam_width/2, height - beam_thickness/2))
right_arm = arm.translate((-arm_offset_x + 20, width/2 - beam_width/2, height - beam_thickness/2))

# 3. Diagonal Braces (The large angled supports)
# Calculate geometry for the brace
brace_height_start = height * 0.75
brace_arm_dist = top_arm_length * 0.6
brace_len = sqrt(brace_height_start**2 + brace_arm_dist**2) # Approximate length needed
brace_angle_val = degrees(atan2(brace_height_start, brace_arm_dist))

# Create a generic brace beam
main_brace = make_beam(200, beam_width, beam_thickness) # Length is approximate, we'll cut it or position it
# Rotate and position
# The brace connects the vertical post (lower down) to the horizontal arm (further out)
brace_rot = main_brace.rotate((0,0,0), (0,1,0), -45) # Approx 45 degrees

# Position left brace
# Start near middle of post, go up to arm
left_brace = brace_rot.translate((-60, -width/2 + beam_width/2, height - 60))
right_brace = brace_rot.translate((-60, width/2 - beam_width/2, height - 60))

# 4. Base Structure
# Horizontal beams at the bottom
base_beam = make_beam(base_length, beam_width, beam_thickness)
base_offset_x = (base_length/2) - (beam_thickness/2)
left_base = base_beam.translate((-base_offset_x, -width/2 + beam_width/2, beam_thickness/2))
right_base = base_beam.translate((-base_offset_x, width/2 - beam_width/2, beam_thickness/2))

# Small angled braces at the bottom
small_brace = make_beam(60, beam_width, beam_thickness).rotate((0,0,0), (0,1,0), -45)
left_small_brace = small_brace.translate((-20, -width/2 + beam_width/2, 20))
right_small_brace = small_brace.translate((-20, width/2 - beam_width/2, 20))

# 5. Cross Members (Connecting left and right frames)
# Top cross member (small block near the joint)
top_block = make_beam(beam_thickness, width + 10, beam_width) # Slightly wider than frame
top_cross = top_block.translate((0, 0, height - beam_thickness*1.5))

# Mid cross member (horizontal plank across the braces)
mid_plank = make_beam(beam_thickness, width + 10, beam_width/2)
mid_cross = mid_plank.translate((-40, 0, height - 60))

# Bottom cross member (at the very bottom rear)
bottom_cross = make_beam(beam_thickness, width, beam_width).rotate((0,0,0),(0,0,1), 90)
bottom_cross = bottom_cross.translate((beam_thickness/2, 0, beam_thickness*1.5))

# 6. Ladder Rungs / Steps on the diagonal
# Steps are attached to the diagonal braces
rung_count = 3
rung_spacing = 30
rungs = cq.Assembly()
rung_geo = make_beam(plank_width, width + 20, plank_thickness) # Wide flat planks

start_x = -90
start_z = height - 90

for i in range(rung_count):
    # Position based on index
    # We follow the diagonal line roughly
    pos_x = start_x - (i * 20)
    pos_z = start_z - (i * 20)
    
    rung = rung_geo.translate((pos_x, 0, pos_z))
    # Combine geometry
    if i == 0:
        all_rungs = rung
    else:
        all_rungs = all_rungs.union(rung)

# 7. Floor/Base Planks
base_plank = make_beam(plank_width, width - beam_width, plank_thickness)
base_plank_1 = base_plank.translate((-20, 0, beam_thickness))
base_plank_2 = base_plank.translate((-50, 0, beam_thickness))


# --- Assembly / Union ---

result = (
    left_post
    .union(right_post)
    .union(left_arm)
    .union(right_arm)
    .union(left_brace)
    .union(right_brace)
    .union(left_base)
    .union(right_base)
    .union(left_small_brace)
    .union(right_small_brace)
    .union(top_cross)
    .union(mid_cross)
    .union(bottom_cross)
    .union(all_rungs)
    .union(base_plank_1)
    .union(base_plank_2)
)

# Refinement: Add the reinforcing blocks shown in the image at joints
# Top joint reinforcement (rectangular blocks on the side)
joint_block = make_beam(30, beam_thickness, 15).rotate((0,0,0), (0,0,1), 90)
# Locate near the top T-junction
jb1 = joint_block.translate((-10, -width/2 - beam_thickness/2, height - 10))
jb2 = joint_block.translate((-10, width/2 + beam_thickness/2, height - 10))

# Add joint blocks to result
result = result.union(jb1).union(jb2)

# Small detail: The "feet" blocks at the very bottom corners
foot_block = make_beam(15, 15, 20)
foot_l = foot_block.translate((0, -width/2 - 2.5, 10))
foot_r = foot_block.translate((0, width/2 + 2.5, 10))

result = result.union(foot_l).union(foot_r)