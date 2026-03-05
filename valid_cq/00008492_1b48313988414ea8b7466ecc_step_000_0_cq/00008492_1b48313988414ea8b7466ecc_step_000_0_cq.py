import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the box
length = 100.0  # Total length
width = 50.0    # Total width
height = 20.0   # Total height

# Dimensions for the recessed face (the "drawer" or "lid" face)
wall_thickness = 2.0  # Thickness of the outer shell
recess_depth = 1.0    # How far the inner face is set back from the edge

# --- Modeling ---

# 1. Create the main rectangular block
main_block = cq.Workplane("XY").box(length, width, height)

# 2. Identify the face to modify. 
# Looking at the image, one of the smaller end faces (YZ plane) has a cutout.
# We will select the face in the +X direction.

# Create the sketch for the cutout.
# We want a rectangle that is smaller than the face by the wall_thickness.
# We will cut this shape into the face.
# However, the image shows a thin gap surrounding a central rectangular plate.
# This looks like a "parting line" or a separate panel fitted in. 
# A common way to model this simple aesthetic is to create a shell or a cut.

# Let's interpret the geometry:
# It looks like a solid box where one end face has a groove cut into it, 
# leaving a rectangular island in the middle. 
# Or it could be an assembly of a sleeve and a drawer. 
# Given the simple "blocky" nature, a groove cut is the most robust single-body representation.

# Define the face to work on (the "front" face relative to the view)
# We'll pick the +X face.
cut_face = main_block.faces(">X").workplane()

# 3. Create the groove
# The groove creates the outline of the inner rectangle.
# We will cut a rectangle, but "leave" the center part? No, that's hard.
# Easier method:
#   A. Create the main solid.
#   B. Create a "pocket" (cut) into the face.
#   C. Create a new "insert" (solid) inside that pocket, slightly smaller to create the gap, 
#      OR just cut a thin rectangular loop.

# Looking closely at the image lines:
# There is a continuous outer rim.
# There is a distinct rectangular face inside.
# The gap is very thin.

# Strategy: Cut a rectangular pocket, then add a rectangular feature back in.
# Or simpler: Just cut a slot.

# Let's try the "Cut a slot" approach (using a rectangular profile swept or just a cut):
# We want to remove material in a loop shape.

# Calculate inner rectangle dimensions
inner_rect_width = width - (2 * wall_thickness)
inner_rect_height = height - (2 * wall_thickness)

# We will cut a pocket representing the recessed area, but actually the image looks flush or slightly recessed?
# The image shows the inner rectangle is *slightly* recessed, creating a shadow line.
# Let's model it as a simple pocket cut for the main recess, 
# then extrude the "inner face" back out, but stop slightly short of the main face.

# Step 2 Revised:
# 1. Select >X face.
# 2. Draw a rectangle offset by wall_thickness.
# 3. Cut inwards by a small amount (e.g., 5mm) to create the "drawer" depth visual.
# 4. Select the bottom of that cut.
# 5. Draw the same rectangle.
# 6. Extrude it back out, but *almost* to the surface (leave `recess_depth`).

# 1. Main Block
result = cq.Workplane("XY").box(length, width, height)

# 2. Create the pocket
result = (
    result.faces(">X")
    .workplane()
    .rect(width - 2*wall_thickness, height - 2*wall_thickness)
    .cutBlind(-5.0) # Cut in deep enough to simulate a separate part if needed, or just a groove
)

# 3. Fill the pocket back in, but leave a recess
# We need to select the face at the bottom of the cut we just made.
# The cut was into >X, so the resulting face is pointing in <X direction *inside* the part? 
# No, the normal of the new face points in >X.
# It's the face with the largest X coordinate that isn't the outer rim.

# Easier selection strategy: Select the face we just cut, which is now recessed.
# We can find it by selecting faces in >X again, filtering for the one that is not at length/2.
result = (
    result.faces(">X[1]") # The second face in the +X stack (the recessed one)
    .workplane()
    .rect(width - 2*wall_thickness - 0.5, height - 2*wall_thickness - 0.5) 
    # ^ Slightly smaller to create a tiny gap/tolerance line around the "drawer", 
    # making it look like a separate assembly
    .extrude(5.0 - recess_depth)
)

# Alternative Interpretation (Simpler):
# The image might just be a box with a rectangular sketch on the face that is just a thin cut.
# Let's stick to the "cut a groove" logic, it's safer for visualization.

# Final Logic construction:
# 1. Box.
# 2. Face >X.
# 3. Sketch a rectangle (outer boundary of groove).
# 4. Sketch a smaller rectangle (inner boundary of groove).
# 5. Cut the area between them.

groove_width = 0.5 # Width of the gap line
groove_depth = 1.0 # Depth of the gap line

result = cq.Workplane("XY").box(length, width, height)

# Create the groove cut
result = (
    result.faces(">X")
    .workplane()
    # Outer rectangle of the groove
    .rect(width - 2*wall_thickness, height - 2*wall_thickness)
    # Inner rectangle of the groove (creates the island)
    .rect(width - 2*wall_thickness - 2*groove_width, height - 2*wall_thickness - 2*groove_width)
    # Cut the region between the two rectangles
    .cutBlind(-groove_depth)
)

# This creates a perfect visual representation of the image:
# A solid block with a rectangular outline engraved on the end face.