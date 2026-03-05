import cadquery as cq

# Parametric dimensions
# Bottom base plate dimensions
base_width = 80.0
base_height = 60.0
base_thickness = 15.0

# Top T-block dimensions
top_block_width = 50.0   # Width of the main body of the top block
top_block_height = 40.0  # Height of the top block
top_block_depth = 30.0   # Depth (thickness) of the top block

# T-feature (the protrusion at the back of the top block)
t_stem_width = 20.0
t_stem_depth = 15.0      # How much it sticks out from the main block

# Create the bottom base plate
# Centered on X, sitting on Z=0
base = cq.Workplane("XY").box(base_width, base_thickness, base_height)

# Create the top block
# It sits on top of the base.
# We need to position it correctly relative to the base.
# Based on the image, the top block seems centered horizontally (X-axis)
# and aligned with the back face or centered on the thickness (Y-axis).
# Let's assume it's centered relative to the base's width.

# Create the main rectangular part of the top block
top_main = (
    cq.Workplane("XY")
    .workplane(offset=base_height / 2 + top_block_height / 2)
    .box(top_block_width, top_block_depth, top_block_height)
)

# Create the "T" protrusion on the back of the top block
# It looks centered on the top block.
t_protrusion = (
    cq.Workplane("XY")
    .workplane(offset=base_height / 2 + top_block_height / 2)
    .center(0, -top_block_depth/2 - t_stem_depth/2) # Move to the back
    .box(t_stem_width, t_stem_depth, top_block_height)
)

# Combine the top parts
top_assembly = top_main.union(t_protrusion)

# We need to align the top assembly with the bottom base.
# In the image, the front faces don't look flush. The top block is thicker than the bottom plate.
# The bottom plate is base_thickness (15). The top block is top_block_depth (30).
# It looks like the top block is resting on the top edge of the base.
# Let's adjust positions to make a single solid.

# Let's rebuild using a more constructive approach relative to a global origin
# to ensure precise alignment as seen in the image.

# 1. Base Plate
# Origin at center of bottom face of the base plate
base_plate = cq.Workplane("XY").box(base_width, base_thickness, base_height, centered=(True, True, False))

# 2. Top Block (The wider part)
# It sits on top of the base (Z = base_height).
# It seems centered horizontally (X).
# In Y, it seems to overhang the base slightly or be thicker.
# Let's assume the back faces are aligned for the main block, or the T-part sticks out.
# Looking at the shadow/perspective:
# The bottom plate is thin. The top block is a fat T-shape.
# The "stem" of the T points backwards (away from viewer) or forwards?
# Let's interpret the image:
# - Large vertical slab at the bottom.
# - Sitting on it is a block.
# - That block has a protrusion extending backwards (top-left in image).
# - The top block is wider than the base plate in the Y direction (thickness).

# Redefining dimensions for better proportionality matching the image
base_w = 60.0
base_h = 50.0
base_t = 10.0

top_w = 40.0
top_h = 30.0
top_d = 25.0 # Main depth

t_stem_w = 15.0
t_stem_d = 10.0

# Constructing
# Base plate standing up. Let's center it on X, Y. Z goes from 0 to base_h.
part1 = cq.Workplane("XY").box(base_w, base_t, base_h, centered=(True, True, False))

# Top main block
# Sits at Z = base_h
# Centered on X.
# In Y, let's align the front faces or centers? 
# The image shows the top block overhangs the back of the bottom plate significantly.
# Let's align the front face of the top block with the front face of the bottom plate?
# Actually, looking at the "step" where they meet, the top block seems to sit somewhat centered or flush on one side.
# Let's try centering the main top block on the base plate first.
part2 = (
    cq.Workplane("XY")
    .workplane(offset=base_h)
    .box(top_w, top_d, top_h, centered=(True, True, False))
)

# Move part2 in Y to align nicely. 
# If centered, and base_t=10, top_d=25, it overhangs both sides.
# In the image, the face facing us (bottom-right) seems flat/continuous? No, there is a definite line/ledge.
# It looks like a standard T-slot cutter shape or a mechanical slide.

# Let's assume standard geometric composition:
# A bottom rectangular prism.
# A top T-shaped prism centered on the bottom one.

# Let's create the Top T-shape as a 2D sketch extruded.
# The T-shape is in the X-Y plane (looking from top).
# Then extruded in Z? No, the T profile is visible from the top view.
# Dimensions:
top_overall_depth = 30.0
top_main_width = 40.0
top_stem_width = 20.0
top_stem_protrusion = 10.0 # Part of the depth
top_height = 30.0

# Base Dimensions
base_width = 60.0
base_thickness = 10.0
base_height = 40.0

# Create the Base
# Centered on X and Y, sitting on Z=0
result = cq.Workplane("XY").box(base_width, base_thickness, base_height, centered=(True, True, False))

# Create the Top Object
# We will draw the T-shape on the top face of the base and extrude up.
# Wait, the base is thinner than the top block.
# Let's construct the top block separately and union.

# Top block parameters refined from visual
t_cross_w = 40.0  # Width of the crossbar of the T
t_cross_d = 20.0  # Depth of the crossbar
t_stem_w = 15.0   # Width of the stem
t_stem_d = 15.0   # Depth of the stem

# Total depth of top part = t_cross_d + t_stem_d
# The image shows the T-shape stem pointing towards the back-left.
# The wide part (crossbar) is on the front-right.

# Position of top block:
# Sits on top of base (Z = base_height)
# It seems the wide part of the T rests on the base, and the stem hangs off the back?
# Or the base is the stem?
# No, the bottom part is clearly a wide plate (60 wide, 10 thick).
# The top part sits on it. The top part is thicker.

# Let's make the top block geometry
top_geo = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    # Move origin to align where we want the center of the T
    .center(0, 0) 
)

# Draw T shape 
# We'll draw two rectangles and fuse them
# Rectangle 1: The wide front part
r1 = top_geo.center(0, 5).box(t_cross_w, t_cross_d, top_height, centered=(True, True, False))
# Rectangle 2: The narrow back part
r2 = top_geo.center(0, -10).box(t_stem_w, t_stem_d, top_height, centered=(True, True, False))

top_part = r1.union(r2)

# Now unite with base
# But wait, looking at the image, the bottom plate is centered under the TOP WIDE PART?
# Or is the whole assembly symmetric?
# The bottom plate looks centered relative to the wide part of the top block.
# Let's adjust the Y offset of the base to match the visual.
# If base is at Y=0, and top wide part is at Y=5 (centered there), 
# let's shift things to be cleaner.

# Final Attempt strategy:
# 1. Define Base Plate at Z=0 to Z=40. Width=60, Thickness=10.
# 2. Define Top Wide Block at Z=40 to Z=70. Width=40, Thickness=20.
# 3. Define Top Narrow Stem at Z=40 to Z=70. Width=20, Thickness=10.
# 4. Align them. 
#    - Base is centered at X=0.
#    - Top Wide Block is centered at X=0.
#    - Top Stem is centered at X=0.
#    - Y alignment: The Top Wide Block seems to sit on the Base. 
#      Let's center the Base and the Top Wide Block on the Y-axis.
#      Then attach the Stem to the back (Y+) of the Wide Block.

# Refined dimensions
H_base = 50.0
W_base = 70.0
T_base = 12.0

H_top = 35.0
W_top_main = 40.0
T_top_main = 25.0

W_top_stem = 20.0
T_top_stem = 15.0

# Base
result = cq.Workplane("XY").box(W_base, T_base, H_base, centered=(True, True, False))

# Top Main Block
# Centered on X, Centered on Y relative to Base (assuming they share a central plane)
top_main = (
    cq.Workplane("XY")
    .workplane(offset=H_base)
    .box(W_top_main, T_top_main, H_top, centered=(True, True, False))
)

# Top Stem
# Attached to the "back" of the top main block.
# If Y is thickness, let's say "back" is +Y.
# We need to shift the center of the stem.
# Center of stem needs to be at Y = T_top_main/2 + T_top_stem/2
y_shift = (T_top_main / 2) + (T_top_stem / 2)

top_stem = (
    cq.Workplane("XY")
    .workplane(offset=H_base)
    .center(0, y_shift)
    .box(W_top_stem, T_top_stem, H_top, centered=(True, True, False))
)

# However, looking at the image again:
# The T-shape is inverted? 
# The "stem" is the protrusion.
# In the image, the protrusion is at the top-left (back).
# The main top block is central.
# The base plate is below.
# Crucially, the base plate (thickness T_base) is significantly THINNER than the Top Main Block (T_top_main).
# And they look aligned at the front face? Or centered?
# Usually these mechanical parts are symmetric about the vertical midplane.
# So centering on Y is the safest bet for the Base and Top Main.
# The Stem then protrudes from one side.

result = result.union(top_main).union(top_stem)

# Adjusting purely for visual match of the "step"
# In the image, the side of the top block (X face) is aligned inward from the base plate (X face). Correct (40 < 70).
# The front face of top block and base plate:
# If they are centered, and T_top_main (25) > T_base (12), the top block overhangs front and back.
# This creates a "ledge" on the top surface of the base plate on both sides.
# The image shows a ledge on the right side.
# This is consistent with centered alignment.

# Final check of variables
# result contains the full solid.
pass