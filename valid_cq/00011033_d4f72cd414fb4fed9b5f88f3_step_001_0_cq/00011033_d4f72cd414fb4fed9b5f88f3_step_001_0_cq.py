import cadquery as cq

# Parametric definitions
base_width = 30.0    # Width of the main block on the left
base_depth = 50.0    # Depth of the main block on the left
base_height = 20.0   # Height of the main block on the left

conn_width = 10.0    # Width of the connecting bridge section
conn_depth = 50.0    # Total depth (spanning across)
conn_height = 10.0   # Height of the bridge section (appears lower)

# The right side is taller and has a step
right_width = 20.0
right_depth = 50.0   # Length of the right arm
right_base_height = 30.0 # Tallest part

# Gap parameters
gap_width = 5.0     # Width of the gap between left block and right structure

# Step details on the right block
step_depth_start = 20.0 # Distance from back where the step begins
step_height_drop = 10.0 # Amount the step drops down

# Create the main assembly by creating separate parts and combining them
# Or better, draw the profile on the XY plane and extrude, then modify.

# Let's break it down into logical blocks based on the image:
# 1. Left Block: A simple rectangle.
# 2. Right Block: An L-shaped extrusion (tall back, short front).
# 3. Connection: A small bridge joining them, but looking at the image, 
#    it seems more like two main parallel blocks connected by a lower bridge.

# Revised strategy:
# Create the Left Block
left_block = cq.Workplane("XY").box(base_width, base_depth, base_height)

# Create the Right Block
# This block has a "step" in it.
# Let's create a full block first, then cut the step.
right_block_full = cq.Workplane("XY").workplane(offset=right_base_height/2).box(right_width, right_depth, right_base_height)

# Create the cutout (step) on the right block
# The step is on the "front" part of the right block (relative to the camera view).
# Based on image, the front part is lower.
step_cutout = (
    cq.Workplane("XY")
    .workplane(offset=right_base_height - step_height_drop/2) # Position cut at top
    .center(0, -right_depth/2 + step_depth_start/2) # Move to front area
    .box(right_width, step_depth_start, step_height_drop) # Box to subtract
)
right_block_stepped = right_block_full.cut(step_cutout)

# Position the Right Block relative to the Left Block
# Move right block to the right. 
# Total offset = (base_width/2) + gap_width + (right_width/2)
offset_x = (base_width / 2) + gap_width + (right_width / 2)
right_block_positioned = right_block_stepped.translate((offset_x, 0, (right_base_height - base_height)/2))

# Create the Connecting Bridge
# Looking at the image, there is a connection between the two blocks.
# It seems to be flush with the "step" on the right block and connects to the left block.
# It sits in the "gap".
bridge_height = right_base_height - step_height_drop # Height of the lower part of right block
bridge = (
    cq.Workplane("XY")
    .workplane(offset=bridge_height/2)
    .box(gap_width, step_depth_start, bridge_height) # Bridge connects only the front part (low part)
)

# Position the bridge
# X offset is between the centers of the two blocks: (base_width/2) + (gap_width/2)
bridge_x = (base_width / 2) + (gap_width / 2)
# Y offset needs to match the front section. The "front" section in our box logic was negative Y relative to center.
# We need to align the bridge with the "stepped down" part of the right block.
bridge_y = -right_depth/2 + step_depth_start/2

bridge_positioned = bridge.translate((bridge_x, bridge_y, (bridge_height - base_height)/2))


# Wait, looking closer at the image:
# The "bridge" isn't a separate piece, the right block has a lower section that extends *towards* the left block?
# Or maybe it's just two blocks.
# Let's re-read the geometry from the image.
# Left side: Large block.
# Right side: Taller block in back, steps down in front.
# Center: There is a gap between the Left Block and the Right Block's BACK (tall) part.
# BUT, the Right Block's FRONT (low) part seems to extend leftwards to touch the Left Block?
# Or is it a separate small connecting bar?
# It looks like a "Bridge" connecting the Left Block and the Right Block, specifically aligned with the lower step of the right block.
# However, the bridge height (Z) seems lower than the Left Block.
# Left Block Height: ~20
# Right Block Low Step Height: ~20 (looks visually similar to Left Block, maybe slightly different?)
# Bridge Height: Looks significantly lower than the Left Block.

# Let's refine dimensions based on visual proportions.
# Let's assume Left Block is H=20.
# Right Block Tall part is H=30.
# Right Block Low part is H=20.
# Bridge connects the Left Block and Right Block in the "front" area.
# Bridge height looks like H=10.

# Redefining dimensions for better visual match:
L_width = 30
L_depth = 50
L_height = 20

R_width = 20
R_depth = 50
R_tall_height = 35
R_step_length = 25 # Length of the low part
R_step_height = 15 # Height of the low part

Gap = 8

Bridge_width = Gap
Bridge_depth = 10 # It looks like a narrow strip connecting them
Bridge_height = 10 
Bridge_location_y = -10 # Position along the depth

# Let's construct it as a single union of primitive shapes for clarity.

# 1. Left Block
part1 = cq.Workplane("XY").box(L_width, L_depth, L_height).translate((-L_width/2 - Gap/2, 0, L_height/2))

# 2. Right Block (Tall Back Section)
# Back section depth
R_back_depth = R_depth - R_step_length
part2 = (
    cq.Workplane("XY")
    .box(R_width, R_back_depth, R_tall_height)
    .translate((R_width/2 + Gap/2, R_depth/2 - R_back_depth/2, R_tall_height/2))
)

# 3. Right Block (Low Front Section)
part3 = (
    cq.Workplane("XY")
    .box(R_width, R_step_length, R_step_height)
    .translate((R_width/2 + Gap/2, -R_depth/2 + R_step_length/2, R_step_height/2))
)

# 4. Connecting Bridge
# It connects the Left Block to the Right Block (Low Front Section).
# It looks like it sits flush with the front face? No, it's slightly set back.
# Let's assume it connects the middles.
bridge_part = (
    cq.Workplane("XY")
    .box(Gap, R_step_length, Bridge_height) # Spanning the gap
    .translate((0, -R_depth/2 + R_step_length/2, Bridge_height/2)) # Centered in X (gap), aligned Y with front section
)

# Combine everything
result = part1.union(part2).union(part3).union(bridge_part)