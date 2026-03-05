import cadquery as cq

# -- Parameters --
# Main dimensions
thickness = 10.0
height_left = 60.0
width_left = 60.0
height_right = 50.0  # Overall height of the right block
width_right = 20.0   # How far it sticks out to the right
depth_right = 40.0   # The thickness/depth of the right block

# Hole parameters
large_hole_diam = 25.0
small_hole_diam = 6.0
small_hole_spacing = 20.0

# -- Modeling --

# 1. Create the left vertical plate (the one with the large hole)
# We center it on Y to make symmetry easier, but align bottom to Z=0 or similar for logic
# Let's align the corner where the two parts meet at the origin (0,0,0) for easier calculations.
# The plate extends in the -X direction and along the Y axis (or Z axis, let's pick Z for height).

# Let's define the orientation:
# X axis: Left-Right (Left plate goes -X, Right block goes +X)
# Z axis: Up-Down
# Y axis: Thickness/Depth

# Left Plate
left_plate = (
    cq.Workplane("XY")
    .box(width_left, thickness, height_left, centered=(False, True, True))
    .translate((-width_left, 0, 0)) # Move so right face is at X=0
)

# 2. Create the right block
# It attaches at X=0.
right_block = (
    cq.Workplane("XY")
    .box(width_right, depth_right, height_right, centered=(False, True, True))
)

# 3. Create the gusset/chamfer connection
# Looking at the image, there is a triangular transition connecting the thin left plate
# to the thicker right block. It looks like a loft or a specific extrusion.
# However, a simpler way to view it is that the back face is flat (flush).
# Let's assume the back faces (Y+) are flush.
# Wait, looking closely at the image:
# The left plate has thickness `thickness` (e.g., 10).
# The right block is much thicker (e.g., 40).
# They seem aligned at the "back" face (let's call it Y_max).
# Then there is a large chamfer or taper connecting the front face of the left plate
# to the front face of the right block.

# Let's restart the strategy with a unified sketch approach for the top-down profile
# or build it additively.

# Strategy B:
# 1. Left Plate.
# 2. Right Block.
# 3. A triangular fillet/chamfer block in the corner.

# Let's refine the alignment based on the image:
# Let the corner where the plates meet be the origin.
# Left plate extends along -X.
# Right block extends along +Y.
# Vertical is Z.

# Re-evaluating orientation based on standard views:
# Let's make the large flat face with the hole lie in the XZ plane.
# So the left plate is: Width along X, Height along Z, Thickness along Y.

L_plate_W = 60.0
L_plate_H = 60.0
L_plate_T = 10.0

R_block_W = 25.0  # Extension in Y
R_block_H = 45.0
R_block_T = 30.0  # Extension in X

# This interpretation seems slightly off. Let's stick to the visual features.
# Feature 1: A flat plate with a big hole.
# Feature 2: A block perpendicular to it.
# Feature 3: A triangular web/stiffener connecting them.

# Let's build it at the origin (0,0,0).
# Left Plate: Starts at X=0, goes -X. Centered on Z.
left_plate = cq.Workplane("YZ").box(L_plate_H, L_plate_T, L_plate_W, centered=(True, True, False)).translate((0, 0, -L_plate_W))
# This is getting confusing with rotations. Let's use simple extrusions.

# Final Strategy:
# Draw the L-shape from the top (XY plane), extrude up, then cut the slope.
# But the heights are different.
# Okay, separate bodies united.

# Part A: The Left Plate
# Dimensions
p1_len = 60.0 # Length along X axis
p1_height = 60.0 # Z
p1_thick = 10.0 # Y

part_a = (
    cq.Workplane("XY")
    .box(p1_len, p1_thick, p1_height, centered=(False, True, False))
)
# Shift it so the right face is at X=0
part_a = part_a.translate((-p1_len, 0, 0))


# Part B: The Right Block
# It connects at the right end of Part A.
p2_stickout = 25.0 # How far it goes in +X
p2_width = 40.0    # Dimension in Y (Thickness)
p2_height = 45.0   # Z

# It seems the back faces are flush.
# Let's assume the "back" is Y = p1_thick/2
back_y = p1_thick / 2.0

# Create the block
part_b = (
    cq.Workplane("XY")
    .workplane(offset=0) # Z=0 base
    .moveTo(0, back_y)
    .lineTo(0, back_y - p2_width)
    .lineTo(p2_stickout, back_y - p2_width)
    .lineTo(p2_stickout, back_y)
    .close()
    .extrude(p2_height)
)

# Part C: The "Gusset" / Slope
# There is a triangular slope connecting the thin face of Part A to the thick face of Part B.
# Looking at the image, the top face of the connection slopes down from Part A (Height 60)
# to Part B (Height 45).
# AND the front face slopes from the thin plate (Thick 10) to the thick block (Width 40).
# Actually, looking at the topology:
# The left plate is just a rectangular prism.
# The right block is a rectangular prism.
# There is a transition piece.
# The transition piece seems to be a loft or a wedge.

# Let's try a different approach: Build the basic L-shape first, then apply cuts/chamfers.

# 1. Base L-shape
# Left arm: 60x10, height 60
# Right arm: 25x40, height 45 (but starts at corner)
# The corner is X=0.

# Left Arm
L_arm = (
    cq.Workplane("XY")
    .box(60, 10, 60, centered=(False, True, False))
    .translate((-60, 0, 0))
)

# Right Arm (the thick block)
# Let's align the "back" faces (Y positive)
# L_arm extends from Y=-5 to Y=5.
# R_arm should extend from Y=5 down to Y=-35 (width 40).
R_arm = (
    cq.Workplane("XY")
    .box(25, 40, 45, centered=(False, False, False))
    .translate((0, -35, 0)) # Align top-right corner to origin-ish
)
# Re-align R_arm so back face is at Y=5
# Current Y range: 0 to 40. Translate(0, -35, 0) -> -35 to 5. Correct.

# Combine them
base_obj = L_arm.union(R_arm)

# Now, the tricky transition.
# The image shows a smooth face connecting the front-face of the left arm
# to the front-face of the right arm.
# Left arm front face is at Y=-5.
# Right arm front face is at Y=-35.
# The transition starts at some distance along the Left Arm (X < 0).
# Looking at the image, the transition starts right at the inner corner (X=0)
# No, it starts further back on the left arm. 
# Actually, it looks like a simple chamfer/fillet might not work because the heights differ.

# Let's build the "Wedge" that fills the corner.
# Vertices of the wedge:
# 1. (0, -5, 0) - Bottom inner corner of L-arm
# 2. (0, -5, 60) - Top inner corner of L-arm
# 3. (0, -35, 0) - Bottom inner corner of R-arm
# 4. (0, -35, 45) - Top inner corner of R-arm
# 5. (-x_start, -5, 0) ? No, looking at the image, the diagonal cut starts exactly at the corner on the left plate side?
# Actually, it looks like the block is just chamfered.
# Let's look at the "Hypotenuse" face. It connects the edge of the left plate (at X=0, Y=-5)
# to the edge of the right block? No.

# Alternative Interpretation:
# The part is a single block 25 wide (X) x 40 deep (Y) x 45 high (Z).
# Plus a plate 60 long (X) x 10 deep (Y) x 60 high (Z).
# The union creates a step.
# Then a large chamfer is applied to the inner corner.
# Let's try that.

# Re-build
# 1. Left Plate (thin)
plate = cq.Workplane("XY").box(60, 10, 60, centered=(False, True, False)).translate((-60, 0, 0))
# Y range: -5 to 5. X range: -60 to 0. Z range: 0 to 60.

# 2. Right Block (thick)
block = cq.Workplane("XY").box(25, 40, 45, centered=(False, False, False)).translate((0, -35, 0))
# Y range: -35 to 5. X range: 0 to 25. Z range: 0 to 45.

# Union
joined = plate.union(block)

# 3. The Chamfer / Slope
# We need to fill the gap between the plate front face (Y=-5) and block front face (Y=-35).
# The fill seems to start from X=0 and creates a triangular wall.
# But wait, the image shows a continuous slope from the top of the plate (Z=60) down to the top of the block (Z=45).
# AND a slope from the front of the plate to the front of the block.
# This implies a Loft operation.

# Let's define two profiles for a loft.
# Profile 1: On the side face of the left plate, at X=0.
# The profile is the rectangle of the plate cross section: Y from -5 to 5, Z from 0 to 60.
# Profile 2: On the side face of the right block... wait, that's the same plane X=0.
# They are joined.

# Let's look at the "Web" or "Transition".
# It looks like a triangle added in the corner defined by planes X=0 and Y=-5.
# Points:
# Top point on Left Plate: (0, -5, 60) -> This is the top-front corner of the joining face.
# Top point on Right Block: (0, -35, 45) -> Top-front corner of the block.
# Bottom point: (0, -35, 0) and (0, -5, 0).
# This forms a quad on the X=0 plane.
# However, the material needs to taper out to the left or right?
# Looking at the shadow/shading: The face connecting the two parts is angled.
# It connects the vertical edge at (0, -5, z) to the vertical edge at (something, -35, z).
# No, the Right Block is strictly to the right of X=0.
# The Left Plate is strictly to the left of X=0.

# Let's assume the Right Block actually overlaps into negative X?
# Or the Left Plate thickens as it approaches the corner?
# In the image, look at the corner where the hole is. The thickness is constant.
# As it approaches the corner, the thickness increases on the bottom side (a triangular fillet)
# and the top side slopes down.

# It is likely a Loft.
# Let's place a sketch on X = -15 (arbitrary start of transition on plate).
# Sketch is simple rectangle 10x60.
# Let's place a sketch on X = 0 (interface).
# Sketch is the profile of the block: 40x45 (aligned correctly).
# Then loft.
# But the plate is straight for most of its length.

# Revised Geometry Plan:
# 1. Create Left Plate (constant section).
# 2. Create Right Block (constant section).
# 3. Create a triangular filler (chamfer) between Y=-5 (plate front) and Y=-35 (block front).
#    This filler is bounded by X=0 plane?
#    Looking closely at the junction: There is a diagonal line.
#    This line goes from (X=0, Y=-5, Z=?) to (X=0, Y=-35, Z=?).
#    This suggests the transition happens entirely within the geometry, or is cut away.

# Let's try "Loft" logic again.
# The Left part ends at X=0. Its face is Rectangle((-5,0) to (5, 60)).
# The Right part starts at X=0. Its face is Rectangle((-35,0) to (5, 45)).
# Since they share the X=0 plane, there is a step change.
# The image shows a SMOOTH transition, essentially a face connecting the edge (-5, 60)
# to (-35, 45).
# And another face connecting (-5, 0) to (-35, 0).

# This creates a transition solid.
# Let's define the points for a customized solid in the corner (the web).
# It's a polyhedron.
# Vertices:
# Common back edge: (0, 5, 0) and (0, 5, 60).
# Wait, the back is flat.
# Top-Front Left: (0, -5, 60)
# Top-Front Right: (0, -35, 45)
# Bottom-Front Left: (0, -5, 0)
# Bottom-Front Right: (0, -35, 0)
# Plus the back vertices (0, 5, 60), (0, 5, 45), (0, 5, 0).
# This is physically impossible if X is 0 for all of them.
# The "Slope" must span some X distance.
# Looking at the image, the angled face starts at X=0 and goes into the block (Positive X).
# So the block is not a simple extrusion. The block has a tapered face on the left side.

# CORRECT INTERPRETATION:
# 1. Left Plate: 60x10x60. Position: X[-60, 0], Y[-5, 5], Z[0, 60].
# 2. Right Block: 25x40x45. Position: X[0, 25], Y[-35, 5], Z[0, 45].
# 3. The "Transition" is a loft/chamfer operation on the Right Block.
#    The Left face of the Right Block (at X=0) must match the Right face of the Left Plate.
#    Left Plate Face: Y[-5, 5], Z[0, 60].
#    Right Block Left Face (idealized): Y[-35, 5], Z[0, 45].
#    They don't match.
#    So, we need a transition shape.
#    The image shows the transition is actually *material added* to the corner.
#    Or the block is cut.
#    Actually, looking at the intersection line on the surface:
#    It travels from the corner of the plate (X=0, Y=-5, Z=0) up to (X=0, Y=-5, Z=some_point).
#    Then it angles towards the block.

# Let's try a Subtractive approach.
# Build the union of the two max bounding boxes.
# Block 1: Left Plate.
# Block 2: Right Block (full size).
# Then apply a "Loft Cut" or "Chamfer" to smooth the step.

# Even simpler:
# 1. Create Left Plate.
# 2. Create Right Block.
# 3. Create a Loft between the rectangular face of the Plate (at X=0)
#    and the rectangular face of the Block (at some X offset? No, the block starts at X=0).
#    Wait, if the block starts at X=0, the step is instantaneous.
#    The image shows a slanted face. This implies the Right Block *is* the slanted part?
#    No, the Right Block has a flat front face further right.
#    So the Right Block has two sections: a transition section and a constant section.

# Let's assume the transition length is `trans_len`.
# Left Plate (X < 0).
# Transition (0 < X < trans_len).
# Right Block Constant (X > trans_len).

# Dimensions estimation:
# Left Plate Length: 60 (visual).
# Right Block Length: 20 (visual).
# Transition Length: It looks sharp. It looks like the transition happens AT the plane X=0, 
# meaning the points are connected directly.
# BUT, looking at the top edge of the transition... it goes from Z=60 to Z=45.
# And the front edge goes from Y=-5 to Y=-35.
# This creates a specific ruled surface.
# This ruled surface is bounded by X=0 on the left?
# If so, the transition cuts into the Right Block.

# Let's model the Right Block as a Loft.
# Profile 1 (at X=0): Matches the Left Plate?
#    Rectangle: Y in [-5, 5], Z in [0, 60].
#    But wait, the back is flush (Y=5).
#    So Profile 1 is: width 10 (Y from -5 to 5), height 60.
# Profile 2 (at X=trans_len?):
#    The image shows the block becomes full size immediately? No.
#    It looks like the block starts at X=0 with the profile of the plate, 
#    and expands to the full profile of the block over some distance.
#    Let's guess the transition length is about 20mm.
#    And then maybe a straight section.

# Let's refine the "Loft" idea.
# Plane A at X=0.
# Plane B at X=20 (end of slope).
# Profile A: Rectangle centered on Y=0? No.
#   Back face is aligned. Let's use `anchored` rects.
#   Back face at Y=0.
#   Profile A (Left Plate interface): Width 10, Height 60. (Extending Y: 0 to -10)
#   Profile B (Right Block start): Width 40, Height 45. (Extending Y: 0 to -40)
# Loft from A to B.
# Then extrude Profile B for the rest of the block length.

# This seems most plausible and robust.

# Dimensions:
# Left Plate: 60 long, 10 thick, 60 high.
# Transition: 25 long. (The slope part).
# Right Block straight part: 15 long.
# Total Right side length ~ 40.

# Holes:
# Large hole in Left Plate.
# Two small holes in Right Block (straight part).

result = (
    cq.Workplane("YZ") # Y is horizontal (thickness), Z is vertical
    .workplane(offset=-60) # Start at far left
    .box(60, 10, 60, centered=(False, True, False)) # Left plate body
    # Wait, box orientation in YZ plane is weird.
    # Let's stick to XY plane and extrude up.
)

# -- Final Code Construction --

# Parameters
L_len = 60.0
L_thick = 10.0
L_height = 60.0

R_trans_len = 20.0 # Length of the sloped section
R_straight_len = 20.0 # Length of the blocky section with holes
R_thick = 35.0 # Total thickness of right block
R_height = 45.0

# Back face alignment: Y=0.
# Front faces extend into -Y.

# 1. Left Plate
# Extrude rectangle 10x60.
# Position: X from -60 to 0.
# Center of plate thickness at Y = -L_thick/2
pt_L = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(0, -L_thick)
    .lineTo(-L_len, -L_thick)
    .lineTo(-L_len, 0)
    .close()
    .extrude(L_height)
)

# 2. Transition Section (The Loft)
# From X=0 to X=R_trans_len
# Profile at X=0: Rectangle(10, 60)
# Profile at X=R_trans_len: Rectangle(R_thick, R_height)
# Note: Back face (Y=0) is shared.

# Using separate workplane for the loft
loft_start = (
    cq.Workplane("YZ")
    .workplane(offset=0) # X=0
    .moveTo(0, 0)
    .lineTo(0, L_height)
    .lineTo(-L_thick, L_height)
    .lineTo(-L_thick, 0)
    .close()
)

loft_end = (
    cq.Workplane("YZ")
    .workplane(offset=R_trans_len) # X=20
    .moveTo(0, 0)
    .lineTo(0, R_height)
    .lineTo(-R_thick, R_height)
    .lineTo(-R_thick, 0)
    .close()
)

# CadQuery loft requires wires on the stack.
# We can do this by constructing a new workplane and adding the wires.
trans_solid = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .moveTo(0,0).lineTo(-L_thick,0).lineTo(-L_thick, L_height).lineTo(0, L_height).close()
    .workplane(offset=R_trans_len)
    .moveTo(0,0).lineTo(-R_thick,0).lineTo(-R_thick, R_height).lineTo(0, R_height).close()
    .loft()
)


# 3. Right Straight Block
# Extrude R_thick x R_height for length R_straight_len
# Starts at X=R_trans_len
pt_R = (
    cq.Workplane("XY")
    .workplane(offset=0) # Z=0
    .moveTo(R_trans_len, 0)
    .lineTo(R_trans_len, -R_thick)
    .lineTo(R_trans_len + R_straight_len, -R_thick)
    .lineTo(R_trans_len + R_straight_len, 0)
    .close()
    .extrude(R_height)
)

# Union all
body = pt_L.union(trans_solid).union(pt_R)

# 4. Holes
# Large hole on Left Plate
# Center approx: X = -30, Z = 30.
body = (
    body.faces(">Y").workplane() # Select the back face (Y=0) or front? 
    # Let's select the XZ plane for positioning to be safe
    .workplane(centerOption="ProjectedOrigin")
    .moveTo(-L_len/2, L_height/2)
    .circle(12.5) # Diameter 25
    .cutThruAll()
)

# Small holes on Right Block
# Located on the flat front face of the right block?
# In the image, the holes are on the flat face at the end (X positive).
# Face normal is +X.
# No, looking at the image, the holes are on the SIDE face (the face normal to X axis? No).
# The holes are on the face parallel to the screen plane in the right section.
# That face is the one with normal +X.
# Let's look at the perspective.
# Left plate is in XZ plane.
# Right block sticks out towards us.
# The holes are on the end face of the right block (Normal +X).

# Hole parameters
h1_z = 15.0
h2_z = 30.0
h_y_offset = -R_thick / 2.0 # Centered in thickness
h_diam = 6.0

body = (
    body.faces(">X").workplane()
    .moveTo(h_y_offset, h1_z)
    .circle(h_diam/2)
    .moveTo(h_y_offset, h2_z)
    .circle(h_diam/2)
    .cutThruAll()
)
# Wait, cutThruAll on >X face goes -X. This will cut through the whole block length.
# Correct.

# Refinement on Hole locations.
# The `moveTo` on a workplane based on >X face:
# The local X is likely global Y? Or global Z?
# Usually: X axis of plane is aligned with one of the global axes.
# Let's be explicit with center.
body = (
    body.faces(">X").workplane(centerOption="CenterOfBoundBox")
    # Workplane origin is now center of the face (X_max, -R_thick/2, R_height/2)
    # Local X is usually along global Y (reversed?), Local Y along Global Z.
    .pushPoints([(0, -10), (0, 10)]) # Just guessing relative positions
    .circle(h_diam/2)
    .cutThruAll()
)

# Let's use absolute coordinates for robustness.
# We want holes at x = R_total, y = -R_thick/2, z = some_z
# We can cut from Y axis side if we want, but image shows holes on the end face.
result = body

# Double check dimensions and constraints
# Left Plate: 60x60x10.
# Transition: 20mm long X-wise.
# Right Block: 20mm long X-wise, 35mm thick, 45mm high.
# Total X = 40 (Right side).
# Total Y = 35.
# Total Z = 60.

# Corrections:
# The transition in the image looks like it has a specific triangular fillet.
# My loft approach approximates it well.
# The back face is flat (Y=0).
# The front face tapers from Y=-10 to Y=-35.
# The top face tapers from Z=60 to Z=45.
# This creates the exact geometry seen.

# Final Code Assembly
# Imports, Vars, Steps.