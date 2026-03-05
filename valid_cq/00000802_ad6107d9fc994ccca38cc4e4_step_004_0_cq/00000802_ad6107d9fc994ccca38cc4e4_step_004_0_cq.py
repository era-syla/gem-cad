import cadquery as cq

# Parametric dimensions
thickness = 10.0
overall_height = 120.0
back_plate_width = 40.0
top_flange_length = 50.0  # From back of plate to front
side_flange_width = 25.0  # The width of the side flange with the big cutout

top_hole_diameter = 6.0
side_hole_diameter = 6.0

big_cutout_radius = 25.0
big_cutout_center_y_offset = -20.0 # From center of main vertical section

# Construct the base shape
# We'll build this as an assembly of parts or a single sketch extrusion.
# A single sketch extrusion from the side profile seems hardest because of the L-shape on top.
# Let's try building the back plate, then the side flange, then the top flange.
# Or better, draw the "L" shape profile from the top view and extrude down, then add the side plate?
# Let's try a constructive approach:
# 1. Back plate (vertical)
# 2. Top flange (horizontal, sticking out)
# 3. Side flange (vertical, perpendicular to back plate) - actually, looking closely, the side flange and back plate seem to be one continuous L-profile from the top view.

# Let's re-examine the geometry.
# It looks like an "L" angle bracket that has been modified.
# The main vertical spine has a width (let's say X) and thickness (Y).
# There is a top horizontal leg.
# There is a side vertical leg that comes off the main spine.

# Let's simplify:
# It is essentially a C-channel or U-channel where one side has been cut away significantly.
# Let's model it as a base L-profile (Top View) extruded downwards, then cut.

# Dimensions derived from estimation:
height = 100
width = 50      # X direction
depth = 40      # Y direction
thick = 8

# Let's try a different approach: Sketching the profile on the XY plane (Top view)
# It looks like an L-shape:
#  _________
# |         |
# |      ___|
# |     |
# |     |
# |_____| 
#
# Then extrude this down.
# Then add the top horizontal part? No, the top part is part of the "L".

# Let's build it piece by piece using the "center" as the reference for the back corner.

# 1. The Main Vertical Back Plate
back_plate = cq.Workplane("YZ").workplane(offset=-width/2).box(depth, height, thick, centered=(True, True, True))
# This is tricky to orient mentally. Let's use standard XYZ.

# Let's define the L-shape from the top (XY plane) and extrude up.
# Wait, the image shows a vertical back plate, a top horizontal plate, and a side vertical plate.
# Actually, looking at the corner, it looks like a bent sheet metal part or a milled block.
# Let's assume the "back" is the face with the single hole on the left in the image.
# The "side" is the face with the two holes and the big cutout.
# The "top" connects them.

# Revised Strategy:
# 1. Create the Back Plate (Left side in image, small arm).
# 2. Create the Side Plate (Right side in image, long arm with cutout).
# 3. Create the Top Plate connecting them.

# Parametric approach
wall_thickness = 10.0
bracket_height = 110.0
bracket_width = 60.0    # "Side plate" width
bracket_depth = 40.0    # "Back plate" depth (length of the short arm)

# Create the base block
# Draw the "L" profile on the top plane
L_sketch = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(bracket_width, 0)
    .lineTo(bracket_width, wall_thickness)
    .lineTo(wall_thickness, wall_thickness)
    .lineTo(wall_thickness, bracket_depth)
    .lineTo(0, bracket_depth)
    .close()
)

# Extrude the basic L-shape down
# However, the image shows the "Back plate" (short arm) only exists at the very top?
# No, looking at the left side of the image, the short arm goes down a bit, then stops?
# Ah, looking closely:
# The shape is an inverted "U" or "C" channel at the top, but the left leg is short.
# And the right leg is long.
# Let's look at the shading.
# Left part: A vertical wall.
# Top part: A horizontal wall connecting left and right.
# Right part: A long vertical wall with holes and cutout.
#
# AND, the left part is short (only at the top).
# No, looking at the bottom of the left part, it ends abruptly.
# It looks like a standard L-bracket where the left leg has been cut short.

# Let's go with:
# 1. Make the Right Plate (the main face).
# 2. Make the Top Plate.
# 3. Make the Left Plate (short).

# Dimensions
H = 120.0  # Total Height
W = 50.0   # Width of the right face
D = 40.0   # Depth (distance between outer faces of left and right plates)
T = 10.0   # Thickness of material

# 1. Right Plate (The long face with the arc cutout)
right_plate = (
    cq.Workplane("YZ")
    .workplane(offset=D/2 - T/2)
    .box(W, H, T, centered=(True, True, True))
    .rotate((1,0,0), (0,1,0), 90) # Rotate to stand up
)
# Currently box is W (y), H(z), T(x) centered.
# Let's just draw on standard planes.

# New Attempt - Logic:
# Draw the profile from the FRONT view (looking at the U-shape end).
# It's an inverted U-shape.
# Extrude it backwards to form the depth.
# Then cut away the material from the short leg.
# Then cut the circle and holes.

# Dimensions
total_width = 50.0   # Width of the U-profile
total_height = 40.0  # Height of the U-profile (the short dimension in the image?)
# No, the image is tall.
# Let's assume:
# Z is vertical (Height).
# X is left-right.
# Y is depth.

height = 120.0
width = 60.0      # The wide plate
depth = 40.0      # The U-shape depth
thickness = 10.0

# Build the main vertical plate (Right side in image)
main_plate = cq.Workplane("YZ").box(width, height, thickness).translate((0, width/2, height/2))
# Align so Y=0 is the inner face, X=0 is center? No.
# Let's keep it simple. Origin at bottom-right-back corner.

result = (
    cq.Workplane("XY")
    # Base L-profile at the top
    .moveTo(0,0)
    .lineTo(width, 0)       # Right plate outer face
    .lineTo(width, thickness) 
    .lineTo(thickness, thickness)
    .lineTo(thickness, depth) # Left plate inner face
    .lineTo(0, depth)       # Left plate outer face
    .lineTo(0, 0)
    .close()
    .extrude(-height) # Extrude down
)

# Now we have a full length L-bracket extruded down.
# The image shows the "left" leg (depth direction in my sketch) is short.
# It only exists at the top. Let's say top 30mm.
cut_height = height - 40.0 # Keep top 40mm

# Cut the left leg (the one along Y axis in sketch)
# The left leg corresponds to the rectangle from (0,0) to (thickness, depth)
# We want to remove material below Z = -40
# The left leg is bound by X in [0, thickness] and Y in [thickness, depth] roughly (based on winding)
# My sketch:
# (0,0) -> (width, 0) is the "back" of the L
# (0, depth) is the tip of the short leg
# Wait, let's re-orient to match image.
# Image: 
# Vertical long plate is on the Right.
# Top plate connects them.
# Short plate is on the Left.

# Let's rebuild properly aligned.
# X axis points Right.
# Z axis points Up.
# Y axis points Back/Into screen.

L_thickness = 10.0
overall_height = 120.0
long_flange_width = 50.0  # The face facing us
short_flange_depth = 40.0 # The depth
short_flange_length = 35.0 # Length of the short leg down from top

# Create the full solid as if both legs were full length first? No, easier to compose.

# 1. Long Plate (Right side)
long_plate = (
    cq.Workplane("YZ")
    .box(long_flange_width, overall_height, L_thickness)
    .translate((-L_thickness/2, 0, 0)) # Shift to align
)

# 2. Top Plate
top_plate = (
    cq.Workplane("XY")
    .box(short_flange_depth, long_flange_width, L_thickness)
    .translate((-short_flange_depth/2 + L_thickness/2, 0, overall_height/2 - L_thickness/2))
)
# Orientation of top plate box: X=depth, Y=width.
# We need to be careful with overlaps. Union will handle it.

# 3. Short Plate (Left side)
short_plate = (
    cq.Workplane("YZ")
    .box(long_flange_width, short_flange_length, L_thickness)
    .rotate((0,1,0), (0,0,0), 90) # Rotate to be perpendicular
    .translate((-short_flange_depth + L_thickness/2, 0, overall_height/2 - short_flange_length/2))
)
# This geometric composition is getting messy. 
# Let's do the subtraction method on a single block, it's more robust.

# Define the bounding box
BB_width = 50.0    # X
BB_depth = 40.0    # Y
BB_height = 120.0  # Z
wall = 10.0

# Start with the Long Plate (Back face in a generic view)
# Let's orient exactly like the image.
# Origin at bottom-right corner of the main long plate.
base = cq.Workplane("XY").box(BB_width, wall, BB_height).translate((-BB_width/2, wall/2, BB_height/2))

# Add top flange
top = (
    cq.Workplane("XY")
    .workplane(offset=BB_height - wall)
    .moveTo(0,0) # At corner
    .lineTo(-BB_width, 0)
    .lineTo(-BB_width, BB_depth)
    .lineTo(0, BB_depth)
    .close()
    .extrude(wall)
)

# Add short side flange (downwards from top)
short_leg_len = 40.0
short_leg = (
    cq.Workplane("XY")
    .workplane(offset=BB_height - wall)
    .moveTo(-BB_width, BB_depth) # Back left corner
    .lineTo(0, BB_depth)
    .lineTo(0, BB_depth - wall)
    .lineTo(-BB_width, BB_depth - wall)
    .close()
    .extrude(-short_leg_len)
)

# The image shows an L-bracket shape where the "short leg" is actually the one on the left.
# My "top" code made a full plate.
# Let's restart with a simpler logic: Start with the side profile (an inverted U) and extrude.
# Profile on YZ plane.
#      _______
#     |  _____| -> Top part and Right part (Long)
#     | |
#     | |
#     |_| -> Left part (Short)

res = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(BB_width, 0)         # Top width
    .lineTo(BB_width, -short_leg_len) # Down short side
    .lineTo(BB_width - wall, -short_leg_len)
    .lineTo(BB_width - wall, -wall)   # Up inside short side
    .lineTo(wall, -wall)         # Across top inside
    .lineTo(wall, -BB_height)    # Down long side
    .lineTo(0, -BB_height)       # Bottom of long side
    .close()
    .extrude(BB_depth) # Extrude along X
)
# This creates the shape but sideways.
# Rotate it to stand up.
# Currently: Y is "Right" in image (width), Z is "Down" in image. Extrusion (X) is "Depth".
# We want Z to be Up.

# Let's try again, sketching on XZ plane (Front view).
# Origin at top-left-front corner of the bounding box.
# X is horizontal width.
# Z is vertical height.
# Y is depth.

# Parameters
total_h = 130.0
width = 55.0  # Width of the face with the cutout
depth = 40.0  # Depth of the U-channel
thickness = 10.0
short_leg_h = 40.0

# 1. Create the main shape by drawing the top profile (U-shape) and extruding down
# Then cut away the rest of the short leg.
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(width, 0)
    .lineTo(width, depth)
    .lineTo(width - thickness, depth)
    .lineTo(width - thickness, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, depth)
    .lineTo(0, depth)
    .close()
    .extrude(-total_h)
)

# Now we have a U-channel 130mm long.
# Orientation:
# (0,0) is Top-Left-Front (if looking from top).
# X goes Right.
# Y goes Back.
# Z goes Down.
# The "left" leg in the image corresponds to the segment near X=0.
# The "right" leg corresponds to X=width.
# The "back" wall (connecting them) is near Y=0.
# Wait, looking at image:
# The face with the cutout is a side wall.
# The face with the single hole is the other side wall.
# The connecting face is at the top.
# So it's an inverted U-channel.

# Let's refine the sketch orientation for "Inverted U":
# Draw profile on Front Plane (XZ).
# Extrude along Y (Depth).
# Profile:
#   __________
#  |          |
#  |   _______|
#  |  |
#  |  |
#  |__|

# Sketch on XZ Plane
# Origin at Top-Left corner of the U-shape
res_shape = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(width, 0)          # Top
    .lineTo(width, -total_h)   # Right Leg (Long)
    .lineTo(width-thickness, -total_h)
    .lineTo(width-thickness, -thickness)
    .lineTo(thickness, -thickness)
    .lineTo(thickness, -short_leg_h) # Left Leg (Short)
    .lineTo(0, -short_leg_h)
    .close()
    .extrude(depth) # Extrude "out" towards viewer or into screen
)

# This shape matches the topology.
# Long leg is on the right. Short leg is on the left. Top connects them.
# The "Right Leg" face is at X=width. It faces +X.
# The "Left Leg" face is at X=0. It faces -X.
# The "Top" is at Z=0.
# The extrusion depth is Y.

# Now features.
# 1. Hole in Short Leg (Left).
# Located on the face at X=0.
# Center it on the face.
short_leg_hole_dia = 8.0
res_shape = (
    res_shape.faces("<X")
    .workplane()
    .center(0, -short_leg_h/2 + thickness/2) # Adjust center relative to workplane origin (center of face)
    # The face center is at Z = -short_leg_h/2, Y = depth/2
    # We probably want the hole centered in the "tab".
    # Let's use absolute coordinates to be safe.
    .pushPoints([(depth/2, -short_leg_h/2)]) # Workplane local coords: X is global Y, Y is global Z
    .hole(short_leg_hole_dia)
)

# 2. Features on Long Leg (Right).
# Face at >X.
# Two small holes and one large arc cutout.
long_leg_hole_dia = 6.0
arc_radius = 25.0

# Select the face
long_face = res_shape.faces(">X").workplane()

# The workplane origin is at the center of the face.
# Face bounds: Z from 0 to -total_h. Y from 0 to depth.
# Center is (depth/2, -total_h/2).
# It's easier to reference from the top or bottom using relative coordinates.

# Let's calculate positions.
# Hole 1: Near top.
h1_z = -25.0
h1_y = depth/2

# Hole 2: Below hole 1.
h2_z = -55.0
h2_y = depth/2

# Arc Cutout:
# A semi-circle cutout from the front edge?
# Looking at the image, the cutout is on the "front" edge of the long plate.
# In my model, the "front" is Y=depth (or Y=0 depending on extrusion direction).
# I extruded positive Y. So Y=0 is back, Y=depth is front.
# The cutout seems to be on the edge of the plate, interrupting the straight vertical line.
# It looks like a bite taken out of the plate width.
# Wait, looking at the image again:
# The long plate has a large semi-circular cutout on its LEFT edge (the edge facing the other leg).
# NO, it's on the edge facing the viewer in the isometric view.
# The two holes are vertically aligned.
# The cutout is between the middle hole and the bottom hole?
# Or is it "scooped" out of the side?
# It looks like the cutout is on the vertical edge that is NOT connected to the back wall?
# No, this is a C-channel. Both vertical edges of the long plate are edges.
# One edge connects to the other plates (via the corner).
# The other edge is free.
# The cutout is on the FREE edge.
# In my model (extruded along +Y), the "corner" is at Y=0 (if we assume the back is at Y=0).
# So the free edge is at Y=depth.
# Wait, my previous extrusion logic:
# Profile on XZ. Extruded +Y.
# The "corner" is continuous along Y.
# The U-shape is the profile.
# So the "free edges" are at the bottom of the legs (-Z).
# This contradicts the "side plate" interpretation.

# Let's restart the interpretation of geometry.
# It is an L-bracket (Top view).
# One arm of the L is the "Back" (let's say X-Z plane).
# The other arm is the "Side" (let's say Y-Z plane).
# Top view:
#  |
#  |___
#
# The "Back" arm is the one with the single hole. It is short in the Z direction? No, image shows it short.
# The "Side" arm is the one with 2 holes + cutout. It is tall.
# AND they are connected at the top.
# So it's an inverted L-shape in the Front view?
# No, they are perpendicular plates.
# Let's assume standard Sheet Metal "Corner Bracket".
# Plate A (Left): Vertical.
# Plate B (Right): Vertical, perpendicular to A.
# Plate C (Top): Horizontal, connects top of A and Top of B.
# This forms a corner.

# Let's stick with the "Inverted U profile extruded" model but rotated.
# Let's say the U-profile is in the Horizontal plane (Top View).
# U-shape:
# |_______|
#
# Left leg: Short depth.
# Right leg: Long depth.
# Back: Connects them.
#
# Image check:
# Left plate (Short arm).
# Right plate (Long arm).
# Back plate (Connecting them).
# BUT, the "Back" plate is the top horizontal surface in the image.
# So the U-profile is vertical (Side View).
#
# Let's go with the XZ Plane Sketch Extruded Y logic again, but carefully mapping features.
# Sketch on XZ (Front).
# Origin (0,0,0).
# Top bar: from (0,0) to (width, 0).
# Left leg (Short): Down from (0,0) to (0, -40).
# Right leg (Long): Down from (width, 0) to (width, -120).
# Thickness 10 inside.
#
# Extrude this profile along +Y (Depth) by 40mm.
#
# Result:
# A shape standing up.
# Top face is horizontal.
# Left vertical face (Short).
# Right vertical face (Long).
#
# Feature 1: Hole in Left Leg.
# Face is at X=0 (Outer face) or X=10 (Inner).
# Image shows hole goes through.
# Location: Centered in the 40x40 area roughly.
#
# Feature 2: Holes in Right Leg.
# Face is at X=width (Outer) or X=width-10 (Inner).
# The cutout is the tricky part.
# The cutout is on the "Free edge" of the right leg.
# The right leg is a rectangle in the YZ plane (viewed from right).
# Its bounds are Y=[0, 40], Z=[-120, 0].
# The "Free edges" are the vertical line at Y=0 and Y=40.
# The edges connected to the top are at Z=0.
# The edge at Z=-120 is the bottom.
# The image shows the cutout is on the vertical edge facing the viewer.
# Let's assume the cutout is on the edge at Y=40 (Front).
# It's a semi-circular bite.

# Final Plan:
# 1. Sketch "Inverted Uneven U" on XZ plane.
# 2. Extrude +Y.
# 3. Cut hole in Left Leg (Workplane on face <X).
# 4. Cut holes in Right Leg (Workplane on face >X).
# 5. Cut large semi-circle on Right Leg (Workplane on face >X or just a cylinder cut).

# Dimensions
H_total = 120.0
W_total = 60.0 # Width between outsides of legs
D_total = 40.0 # Extrusion depth
T = 10.0
Leg_Short_H = 40.0

# Radius of big cutout
R_cutout = 30.0

result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(W_total, 0)
    .lineTo(W_total, -H_total)
    .lineTo(W_total - T, -H_total)
    .lineTo(W_total - T, -T)
    .lineTo(T, -T)
    .lineTo(T, -Leg_Short_H)
    .lineTo(0, -Leg_Short_H)
    .close()
    .extrude(D_total)
)

# Left Hole
# Center of the short leg face: Y=D_total/2, Z=-Leg_Short_H/2
result = (
    result.faces("<X").workplane()
    .pushPoints([(D_total/2, -Leg_Short_H/2)]) # Note: local Y is global Z
    .hole(8.0)
)

# Right Side Features
# We need to cut a semi-circle from the "front" edge (Y=D_total).
# And drill two holes.

# Let's locate the cutout. It looks centered vertically on the lower section?
# Or just a big bite.
# Let's place it at Z = -80, radius 25.
# Center of circle is on the edge line (Y=D_total).
# Cutout axis is X axis.

# Using a cylinder to cut the arc is usually robust.
# Cylinder orientation: along X.
# Position: X=any, Y=D_total, Z=-80.
cutout_z = -75.0
cutout_r = 25.0

result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=W_total) # Move to right face
    .moveTo(D_total, cutout_z) # Move to edge
    .circle(cutout_r)
    .extrude(-T * 2) # Cut through inwards
)

# Holes on Right Side
# Top hole
h1_z = -30.0
# Bottom hole (below cutout)
h3_z = -105.0 
# Middle hole (above cutout)
# Image shows:
# Top part (Corner).
# Hole 1.
# Hole 2.
# Cutout.
# Hole 3.
# Wait, look at image again.
# Top corner.
# Hole 1.
# Hole 2.
# BIG CUTOUT.
# Bottom leg continues?
# Actually, the cutout looks like it IS the bottom edge shape, but there is a small tip left?
# Looking at the bottom right of the image:
# There is a square-ish tip at the bottom.
# Above that is the circular cutout.
# Above that is a hole.
# Above that is another hole.
# So: 2 holes, then cutout, then bottom tip with a hole?
# Let's count holes on the long side.
# I see a hole near the top.
# I see a hole in the middle.
# I see the cutout.
# I see a hole at the bottom tip.
# Total 3 holes on the long leg.

# Let's re-read image.
# Short leg: 1 hole.
# Long leg:
#  - Hole near top.
#  - Hole near middle.
#  - Large scallop cut out of the 'front' edge (relative to the camera view).
#  - Hole at the bottom.
# Total 3 holes on long leg.

# Refined positions for Long Leg (Face >X):
# Y center = D_total / 2 (20.0)
# Z positions (from top 0):
# Hole 1: -25
# Hole 2: -50
# Cutout Center Z: -80. Radius ~25.
# Hole 3: -110.

result = (
    result.faces(">X").workplane()
    .pushPoints([
        (D_total/2, -25),
        (D_total/2, -55),
        (D_total/2, -105) # Bottom hole
    ])
    .hole(6.0)
)

# Re-apply the cutout more precisely
# The cutout takes a bite out of the edge at Y=D_total?
# Or Y=0?
# In the image, we see the inner face of the "U".
# The short leg is on the left.
# The long leg is on the right.
# The cutout is on the edge of the long leg closer to the viewer.
# In my extrusion (Extrude +Y), the face closer to viewer (assuming generic ISO view) is usually +Y max.
# So edge at Y=D_total is correct.

# Re-do cutout to be sure it's clean
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=W_total + 10) # Start outside
    .moveTo(D_total, -80) # Center on the edge
    .circle(22.0)
    .extrude(-50) # Cut through
)

# Final check of the bottom tip.
# If Z total is 120, cutout center -80, radius 22 -> cutout goes to -102.
# Hole 3 at -105.
# Bottom at -120.
# Leaves about 18mm at bottom. Looks roughly right.

# One detail: The bottom hole is shown in the image on the little tab remaining after the cutout.
# The cutout goes deep.
# My cutout is centered on the edge Y=40.
# It cuts into the plate.
# The plate is 40mm deep.
# Radius 22 cuts 22mm into the 40mm depth.
# Remaining material width = 18mm.
# The hole should be centered in the remaining material?
# Or aligned with other holes?
# In the image, the bottom hole looks aligned with the top holes vertically.
# If top holes are at Y=20 (mid-depth), and cutout takes away from Y=40 to Y=18.
# Then Y=20 is very close to the cut edge.
# Maybe the cutout radius is smaller, or holes are further back?
# Let's shift holes to Y=15 (closer to back/bend).
# And shift cutout to Y=40, R=25.
# Cut reaches Y=15. That would intersect the hole line.
# Let's move holes to Y=12.
# And cutout R=20. (Reaches Y=20).
# This provides clearance.

# Revised Dimensions
D_total = 40.0
W_total = 50.0 # narrowed slightly
H_total = 120.0
T = 8.0

# Holes X (on the face): 12mm from the corner/bend (Y=12 in my coord system approx)
hole_offset_from_back = 12.0 
# Note: Back is Y=0.
# So hole Y = 12.0

# Cutout
cutout_R = 25.0
cutout_Z = -80.0
# Cutout center is on the front edge Y=D_total.
# It cuts inwards to Y = D_total - 25 = 15.
# If holes are at Y=12, there is 3mm wall. OK.

# Final Code Structure
import cadquery as cq

# Parameters
height = 120.0
width = 50.0  # Width of the main face
depth = 40.0  # Depth of the bracket (the U-profile depth)
thickness = 8.0
short_leg_length = 35.0

# Create the base profile (Inverted U)
# Sketch on XZ plane
# (0,0) is Top-Left
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(width, 0)
    .lineTo(width, -height)         # Right leg outer
    .lineTo(width - thickness, -height)
    .lineTo(width - thickness, -thickness)
    .lineTo(thickness, -thickness)
    .lineTo(thickness, -short_leg_length) # Left leg inner
    .lineTo(0, -short_leg_length)   # Left leg outer
    .close()
    .extrude(depth)
)

# Add Holes to Short Leg (Left side, Face <X)
# Center hole in the face
result = (
    result.faces("<X").workplane()
    .pushPoints([(depth/2, -short_leg_length/2)]) # Y(global), Z(global)
    .hole(6.0)
)

# Add Features to Long Leg (Right side, Face >X)
# Holes aligned near the back spine (closer to Y=0) to avoid the cutout
hole_y_pos = 12.0 # From back edge
cutout_radius = 24.0
cutout_z_pos = -80.0

result = (
    result.faces(">X").workplane()
    # Add 3 holes
    .pushPoints([
        (hole_y_pos, -25.0),
        (hole_y_pos, -50.0),
        (hole_y_pos, -108.0)
    ])
    .hole(6.0)
)

# Add the large cutout
# Cutout is on the "front" edge (Y=depth)
# We use a cylindrical cut
# Orientation: Cylinder along X axis
cut_tool = (
    cq.Workplane("YZ")
    .workplane(offset=width + 10) # Start outside right
    .moveTo(depth, cutout_z_pos)  # Center on the front edge
    .circle(cutout_radius)
    .extrude(-50) # Cut inwards across width
)

result = result.cut(cut_tool)

# Fillets? Image shows sharp corners mostly, maybe very slight radius.
# Let's leave sharp for exactness to "CAD engineer" prompt unless specified.
# The image looks rendered with typical sharp edges.