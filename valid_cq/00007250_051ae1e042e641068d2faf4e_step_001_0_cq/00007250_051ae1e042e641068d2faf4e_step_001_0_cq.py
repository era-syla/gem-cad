import cadquery as cq

# Parametric dimensions
# Overall dimensions of the bounding box
total_height = 80.0
total_width = 40.0
total_length = 80.0

# Thickness of the walls
wall_thickness = 20.0

# Dimensions for the bottom cutout
cutout_width = 15.0
cutout_height = 25.0

# Create the base L-shape
# We'll start by creating a solid block and then cutting away the corner to make the L-shape
# Or better, draw the L-shape profile on the XY plane and extrude up.

# Define the points for the L-shaped profile
# Let's assume the corner is at (0,0)
# (0,0) -> (total_length, 0) -> (total_length, wall_thickness) -> 
# (wall_thickness, wall_thickness) -> (wall_thickness, total_width) -> (0, total_width) -> close

l_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(total_length, 0)
    .lineTo(total_length, wall_thickness)
    .lineTo(wall_thickness, wall_thickness)
    .lineTo(wall_thickness, total_width)
    .lineTo(0, total_width)
    .close()
    .extrude(total_height)
)

# Now create the cutout at the bottom
# The cutout is on the face that corresponds to the short leg of the L, facing "outwards".
# Looking at the coordinates:
# The face is likely at x=0 or y=total_width depending on orientation.
# Let's assume the long part is along X and the short part projects along Y.
# Based on standard isometric views:
# If X is to the right, Y is "back/left", Z is up.
# The image shows a large face on the right and a smaller face on the left.
# The cutout is on the smaller face on the left side of the image.

# Let's adjust orientation to match the image better.
# The image shows a long wall on the right, and a shorter wall projecting to the left.
# The cutout is at the bottom of the "front" face of the left projection.

# Let's rebuild more intuitively relative to the image view.
# Imagine origin at bottom-left-front corner of the L-shape.
block_main = cq.Workplane("XY").box(total_length, wall_thickness, total_height, centered=False)
# Move the main block to the right position relative to the side block
# Let's say the side block is the one with the hole.

# Re-strategy: Union of two boxes
# Box 1 (Right side large wall): 
box1_len = total_length - wall_thickness
box1_wid = wall_thickness
box1_ht = total_height
# Box 2 (Left side wall with hole):
box2_len = wall_thickness
box2_wid = total_width
box2_ht = total_height

# Let's construct it so the corner is at the origin (0,0,0)
# We want the L shape.
part = (
    cq.Workplane("XY")
    .lineTo(total_width, 0)           # Bottom edge of L (short leg width)
    .lineTo(total_width, wall_thickness) # Thickness of short leg
    .lineTo(wall_thickness, wall_thickness) # Inner corner
    .lineTo(wall_thickness, total_length)   # Inner edge of long leg
    .lineTo(0, total_length)          # Top edge of long leg (long leg length)
    .close()
    .extrude(total_height)
)

# Orientation check:
# This creates an L shape on the XY plane.
# Let's rotate it or pick the right face for the cutout.
# The cutout is at the bottom of the face defined by the segment (total_width, 0) to (0,0)? 
# No, looking at the image:
# There is a face facing us (front-left) that has the hole.
# There is a long face receding to the right.

# Let's define the shape based on the image's "front" view
# Left block (with hole): width=20, depth=40, height=80
# Right block: width=60, depth=20, height=80 (attached to the back of the left block)

# Let's try constructing a box and cutting a notch to make the L, then cutting the hole.
# Bounding box:
# Width (X) = total_length (say 80)
# Depth (Y) = total_width (say 40)
# Height (Z) = total_height (say 80)

result = (
    cq.Workplane("XY")
    # Base L-profile
    .moveTo(0, 0)
    .lineTo(total_length, 0)
    .lineTo(total_length, wall_thickness)
    .lineTo(wall_thickness, wall_thickness)
    .lineTo(wall_thickness, total_width)
    .lineTo(0, total_width)
    .close()
    .extrude(total_height)
)

# The cutout is located on the face at X=0.
# It is centered horizontally on that face (width=wall_thickness/20 usually, but visually it looks centered on the protruding part).
# Wait, looking at the image, the cutout is on the face of the short leg of the L.
# In my coordinates above:
# The short leg extends from Y=wall_thickness to Y=total_width at X=0..wall_thickness.
# The face is the one at X=0, spanning Y=0 to Y=total_width? No.
# Let's visualize the profile coordinates again.
# (0,0) is outer corner.
# X axis goes along long leg.
# Y axis goes along short leg.
# The face with the hole is the face at X=0? No, that would be the "back" or "side".
# In the image, the "front" is the corner.
# Let's assume the corner closest to the camera is (wall_thickness, wall_thickness) in "local" terms if we carved it out, 
# but let's stick to the generated geometry.

# With the profile:
# (0,0) -> (total_length, 0) -> ... -> (0, total_width)
# The face at Y=total_width (from X=0 to X=wall_thickness) is a candidate.
# The face at X=total_length is the far end.
# The face at X=0 (from Y=0 to Y=total_width) is a large flat back/side.

# Let's rotate the mental model.
# Long wall is on the right. Short wall on the left.
# Face with hole is on the "front" of the short wall.
# Let's pick the face on the "bottom" of the L-shape profile (Y=0 line?).
# No, let's select the face by normal.
# The face normal vector should be roughly (-1, -1, 0) for an isometric view, but let's select based on position.

# Let's simplify. Build two blocks and union them.
# Block 1 (Long, Right): 
# Position: centered? No.
b1 = cq.Workplane("XY").box(total_length, wall_thickness, total_height, centered=False)
# Block 2 (Short, Left):
# Needs to align with the left end of b1, and protrude forward.
# b1 occupies: x in [0, 80], y in [0, 20], z in [0, 80]
# b2 should occupy: x in [0, 20], y in [20, 40], z in [0, 80]
b2 = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(0, wall_thickness)
    .box(wall_thickness, total_width - wall_thickness, total_height, centered=False)
)

result = b1.union(b2)

# Now select the face for the cutout.
# The cutout is on the front face of b2.
# That face is at y = total_width (if y grows forward? No, usually Y grows 'back' in simple plots, but here Y is depth).
# Based on b2 definition: y ranges from 20 to 40.
# The face is at y = 40 (the "frontmost" face of the short leg in this coord system).
# Let's verify orientations.
# If X is Right, Y is Back, Z is Up.
# b1 is (0,0,0) to (80, 20, 80). Back wall.
# b2 is (0,20,0) to (20, 40, 80). Side extension sticking "further back"? 
# No, normally Y is "up" on paper, but "depth" in 3D.
# Let's assume standard view: X right, Y up/back, Z up.
# Let's put the corner at (0,0).
# Long leg along X. Short leg along Y.
# The face with the hole is at the end of the short leg (Y max) or the side of the short leg (X min)?
# Looking at the image: The "L" is visible from the top. The hole is on the face of the short leg, facing the viewer.
# In the coordinate system where:
# (0,0) is the inner corner.
# Long leg goes +X.
# Short leg goes +Y.
# The hole is on the face at Y_max? Or X_min?
# The image shows the face with the hole is perpendicular to the long wall's face.
# So if long wall face is in XZ plane, hole face is in YZ plane.
# In my union construction:
# b1 faces are Y=0 and Y=20.
# b2 faces are X=0, X=20, Y=20, Y=40.
# The outer faces are X=80, Y=0 (back), X=0 (side), Y=40 (front).
# The image shows a corner. Let's assume the corner closest to us is formed by the planes defining the "inner" L.
# Actually, the image looks like the convex hull is a box, and a chunk is missing (the empty space of the L).
# The hole is on the narrow face of the L-leg.

# Let's assume the face for the hole is the one at X=0 (the side wall).
# b1: (0,0,0) to (20, 80, 80) -- Long leg along Y
# b2: (0,0,0) to (60, 20, 80) -- Short leg along X (protruding right)
# This forms an L.
# Face with hole: The narrow face at the end of the short leg (X=60)? No.
# The image shows the hole on the "thick" part's face? No, on the vertical face.
# Let's look at the proportions.
# Left face (with hole): Looks like width ~20-30.
# Right face (long): Looks like length ~60-80.
# So it's an L-bracket standing up.
# Let's construct it specifically to match the visual orientation.
# Main block (Right): Y-aligned. width=20, length=80, height=80.
# Side block (Left): X-aligned. width=40 (total), length=20, height=80.
# Result is L-shape.
# Cutout is on the front face of the left block.

result = (
    cq.Workplane("XY")
    .moveTo(0,0)
    .lineTo(20, 0)    # Move right
    .lineTo(20, 40)   # Move up (back) - inner corner
    .lineTo(60, 40)   # Move right - along long leg
    .lineTo(60, 60)   # Thickness of long leg
    .lineTo(0, 60)    # Back to left edge
    .close()
    .extrude(80)
)

# Now we need to cut the hole.
# The hole is on the face defined by the segment (0,0) to (20,0) -> Face normal -Y.
# Or segment (0,0) to (0,60) -> Face normal -X.
# Looking at the image, the hole is on the face that is "facing" us on the left.
# If we assume standard isometric:
# Left face is YZ plane (Normal -X or +X).
# Right face is XZ plane (Normal -Y or +Y).
# The hole is on a face with Normal e.g. -Y.
# Let's select the face at the "bottom left" of the L shape in plan view.
# In the code above: the segment (0,0) to (20,0) has Normal (0,-1). This is a front-facing face.
# Width is 20. This matches the "narrow" appearance.
# Cutout is a rectangle at the bottom.

result = (
    result
    .faces("<Y") # Select the frontmost face (y=0)
    .workplane()
    .center(0, -total_height/2 + cutout_height/2) # Move to bottom. Default center is face center (0, 40). We want y=12.5 relative to bottom.
    # Current workplane center is (10, 40) in global coords roughly (mapped to local 2D).
    # Local X is along global X (width 20). Local Y is along global Z (height 80).
    # We want to cut a rect of 15x25 at the bottom.
    .rect(cutout_width, cutout_height)
    .cutThruAll()
)