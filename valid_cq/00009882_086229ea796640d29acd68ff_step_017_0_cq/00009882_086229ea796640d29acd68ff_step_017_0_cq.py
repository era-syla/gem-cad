import cadquery as cq

# --- Parametric Dimensions ---
# Overall block dimensions
block_length = 80.0  # X direction
block_width = 70.0   # Y direction
block_height = 25.0  # Z direction (total)

# The block appears to be split or have a seam in the middle, 
# implying it might be two halves, but for a single solid model, 
# we model it as one block with features.
# Let's assume the seam is at mid-height.
split_z = block_height / 2.0

# Large Central Hole
center_hole_diam = 15.0

# Side through-hole (visible on the right face)
side_hole_diam = 18.0
side_hole_z = split_z

# Top Face Mounting Holes (4 corner pattern)
corner_hole_diam = 4.5
corner_hole_spacing_x = 55.0
corner_hole_spacing_y = 50.0

# Front Mechanism / Slot Area
front_slot_width = 25.0
front_slot_depth = 15.0
front_cutout_height = 12.0 # Height of the rectangular cutout in front face

# Flexure/Slot Cut details
slit_width = 2.0
slit_length = 50.0
slit_offset_y = 15.0 # From the front edge inward

# Clamp screw holes on the front face (left side)
clamp_hole_diam = 4.0
clamp_hole_spacing_z = 10.0

# Top small hole near the slit (clamp actuator?)
top_clamp_hole_diam = 5.0
top_clamp_hole_pos_x = -20.0 # Estimate relative to center
top_clamp_hole_pos_y = -block_width/2 + 10.0 # Near front edge

# Internal cutout for the flexure hinge mechanism
internal_pocket_width = 15.0
internal_pocket_length = 15.0
internal_pocket_depth = block_height - 5.0 # Goes most of the way through

# --- Modeling Strategy ---
# 1. Create the base block.
# 2. Cut the large central vertical hole.
# 3. Cut the large horizontal side hole.
# 4. Create the front "mouth" cutout.
# 5. Create the "L" shaped slit that forms the flexure/clamp mechanism.
# 6. Add the mounting holes on top.
# 7. Add the clamping holes on the front face.
# 8. Add the specific internal cutout visible in the front opening.

# --- CadQuery Construction ---

# 1. Base Block
result = cq.Workplane("XY").box(block_length, block_width, block_height)

# 2. Central Vertical Hole
result = result.faces(">Z").workplane().hole(center_hole_diam)

# 3. Side Horizontal Hole (Right side)
# Positioned on the right face, centered vertically on the "split" line (Z=0 in local coords if box centered on origin?)
# Note: box is centered at origin, so Z extends from -h/2 to h/2.
result = result.faces(">X").workplane().hole(side_hole_diam)

# 4. Front Cutout (The rectangular opening on the -Y face)
# We want to cut a pocket into the front face.
# Let's define the front face as -Y.
result = result.faces("<Y").workplane().center(0, 0).rect(front_slot_width, front_cutout_height).cutBlind(-front_slot_depth)

# 5. The "L" or "T" slit for the flexure.
# Looking at the image, there is a slit running parallel to the front face (-Y),
# separating a thin front section.
# Then there is a perpendicular slit connecting to the front face (left side of the center).
# Actually, it looks like a "U" shape or a simple long slot with a bridge.
# Let's interpret it as a long slot running X-wise, cutting from the top, 
# and a vertical cut splitting the front left corner.

# Slit 1: The long cut parallel to X axis
slit_x_start = -block_length/2
slit_x_end = block_length/2 - 25.0 # Stops before the right side
slit_y_pos = -block_width/2 + 12.0 # Offset from front

# Create a sketch for the slit on top face
slit_sketch = (
    cq.Workplane("XY")
    .workplane(offset=block_height/2)
    .moveTo(slit_x_start, slit_y_pos)
    .lineTo(slit_x_end, slit_y_pos)
    # Give it width to make it a cut
    .rect(slit_x_end - slit_x_start + slit_width, slit_width, centered=False) 
    # Adjust rect so lineTo path is one edge? No, let's just place a rect.
)

# Better approach for the slit: Place a rect center
slit_center_x = (slit_x_start + slit_x_end) / 2.0
slit_rect_len = abs(slit_x_end - slit_x_start)

# Cut the main flexure slit (Top down)
# It goes deep, likely past the horizontal hole or intersects it.
result = result.faces(">Z").workplane().center(slit_center_x + block_length/4 - 12.5, slit_y_pos).rect(slit_rect_len, slit_width).cutBlind(-block_height + 5)


# 6. Top Mounting Holes (4 corners)
# Relative to center
result = (
    result.faces(">Z").workplane()
    .rect(corner_hole_spacing_x, corner_hole_spacing_y, forConstruction=True)
    .vertices()
    .hole(corner_hole_diam)
)

# 7. Clamp Holes on Front Face (Left Side)
# These represent the screws to tighten the flexure.
# They are on the -Y face, on the negative X side.
clamp_x_pos = -block_length/2 + 8.0 # Near left edge
result = (
    result.faces("<Y").workplane()
    .transformed(offset=cq.Vector(clamp_x_pos, 0, 0))
    .pushPoints([(0, clamp_hole_spacing_z/2), (0, -clamp_hole_spacing_z/2)])
    .hole(clamp_hole_diam, depth=20.0) # Depth into the flexure arm
)

# 8. Additional Top Holes
# There is a hole on the flexure arm itself (front left)
result = (
    result.faces(">Z").workplane()
    .moveTo(-block_length/4, slit_y_pos - 6.0) # On the thin strip
    .hole(top_clamp_hole_diam)
)

# There is a vertical cut splitting the flexure arm on the left side?
# Looking closely at the image, the slit goes all the way to the left face (-X).
# We modeled that with the slit_x_start.

# 9. Internal cutout/pocket details
# Inside the front rectangular opening, there's a cylindrical boss or column.
# Let's add that back or refine the cut.
# It looks like the front cutout exposes a cylindrical post related to the central hole?
# No, it looks like a specific mechanism seating.
# Let's add the small vertical cylinder visible inside the front pocket.

pocket_center_z = 0 # Center of block height
pocket_floor_z = -front_cutout_height/2
column_diam = 8.0

# We need to add material back inside the pocket or cut around it.
# Easiest is to cut the pocket, then union a cylinder.
column = (
    cq.Workplane("XY")
    .workplane(offset=pocket_floor_z)
    .moveTo(0, -block_width/2 + front_slot_depth/2)
    .circle(column_diam/2)
    .extrude(front_cutout_height)
)
# Intersection to keep it within the bounds if needed, but simple union works if dimensions align.
# Actually, looking at the image, the front pocket has a specific shape. 
# It cuts in, but leaves a cylindrical boss.
# Let's redo the front cut slightly more specifically to match the image better.

# Refined Front Cut:
# Instead of a simple rect cut, we cut the rect but exclude the cylinder.
# Or, just add the cylinder back.
# The cylinder is located centrally in X, inside the front pocket.
post_y = -block_width/2 + front_slot_depth/2
post_result = (
    cq.Workplane("XY")
    .workplane(offset=-front_cutout_height/2) # Start from bottom of pocket (relative to center Z)
    .moveTo(0, post_y)
    .circle(column_diam/2)
    .extrude(front_cutout_height)
)

# Combine
result = result.union(post_result)

# 10. Split Line (Cosmetic)
# The image shows a horizontal line across the side. 
# In a single solid CAD, this is usually geometry, but could be a small V-groove.
# We will skip cosmetic split lines as this requests a solid model, 
# and the hole creates the functional split visual.

# 11. The vertical slit cut on the front beam
# The slit we made earlier runs parallel to X.
# There is a small perpendicular notch connecting the long slit to the internal pocket?
# Looking at the image:
# The long slit (parallel to front face) has a "hook" at the end near the center.
# It turns 90 degrees towards the back (-Y direction? no, +Y)
# The slit effectively separates the "clamp" arm.
# Let's add the small L-turn to the slit at the right end of the cut.

slit_hook_x = slit_x_end
slit_hook_len = 8.0
slit_hook_width = slit_width

result = (
    result.faces(">Z").workplane()
    .moveTo(slit_hook_x - slit_width/2, slit_y_pos)
    .rect(slit_width, slit_hook_len, centered=False) # Cut towards +Y (back)
    .cutBlind(-block_height/2) # Cut deep enough
)

# 12. Fillets/Chamfers
# There are no heavy fillets visible, edges are sharp.
# The central hole has a chamfer.
result = result.faces(">Z").edges(cq.NearestToPointSelector((0,0))).chamfer(1.0)

# Final check of the slit position.
# The slit is on the left side of the image (since the side hole is on the right).
# In our coordinate system:
# Right face (+X) has the hole.
# Front face (-Y) has the pocket.
# The slit should run from -X towards the center.
# Our code defines slit_x_start = -block_length/2 (Left/Minus X)
# slit_x_end = block_length/2 - 25 (Right/Plus X)
# This matches the image orientation.

# The mounting hole on the flexure arm needs to be a counterbore?
# It looks simple in the image.

# One specific detail: The front left clamp screw holes go through the "loose" part of the flexure
# and tap into the main body?
# In the image, on the left face (-X, not visible directly but implied), or the front face (-Y left side).
# The holes are on the front face (-Y).
# The slit separates this front face region from the main block.
# So the holes go through the front strip.

# Align the specific cutout in the slit.
# The image shows the slit stopping, then a small perpendicular cut going *inward* (away from front edge).
# We added that as 'slit_hook'.

# Ensure the front pocket doesn't destroy the slit logic.
# The front pocket is in the center. The slit runs above it (in Z? No, slit is vertical through cut).
# The slit is offset Y=12, front face is Y=-35.
# Wait, block width is 70. Center is 0. Front face is -35.
# slit_y_pos = -block_width/2 + 12.0 = -35 + 12 = -23.
# The front pocket depth is 15. -35 + 15 = -20.
# The slit (-23) is *inside* the depth of the pocket region (-20).
# This means the slit cuts into the roof of the pocket if the pocket is not a through-cut.
# In the image, the slit is behind the front face wall.
# Let's adjust slit_y_pos to be slightly deeper than the pocket wall thickness.
# If wall is ~8mm thick, slit is at -35 + 8 = -27.
# Pocket depth is 15. The slit is *behind* the pocket?
# Looking at the image, the slit is clearly behind the front face.
# The pocket cuts into the front face.
# The slit is further back.
# Let's adjust slit_y_pos to be -15 (relative to center 0).
# Front face is -35. Pocket back wall is -20.
# Slit at -15 puts it behind the pocket. This looks correct.
# Updated slit_y_pos calculation.

# Recalculate variables for consistency
slit_y_pos = -block_width/2 + 18.0  # -17.0

# Re-running the logic mentally:
# 1. Box.
# 2. Slit at Y = -17.
# 3. Pocket at Front (Y=-35) depth 15 => Back of pocket at Y=-20.
# The slit is at -17, so it is 3mm behind the pocket wall. This is safe and valid.

# Final Code Assembly