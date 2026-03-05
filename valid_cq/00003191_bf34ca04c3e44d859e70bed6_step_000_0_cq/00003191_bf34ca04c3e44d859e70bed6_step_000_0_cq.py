import cadquery as cq

# --- Parametric Dimensions ---
length = 80.0       # Total length of the block
width = 30.0        # Depth/Width of the block
height = 20.0       # Height of the block

# Slot dimensions (bottom face)
slot_width = 6.0
slot_depth = 4.0

# Hole dimensions (side face)
hole_diameter = 4.0
cbore_diameter = 7.0
cbore_depth = 3.0
hole_spacing = 50.0 # Distance between hole centers
hole_height_offset = height / 2.0 # Vertically centered

# --- Model Construction ---

# 1. Create the base block
# We center it on X and Y to make symmetry operations easier
result = cq.Workplane("XY").box(length, width, height)

# 2. Cut the slot on the bottom
# We select the bottom face ("<Z"), sketch a rectangle, and cut it blind
result = (
    result
    .faces("<Z")
    .workplane()
    .center(0, 0) # Ensure we are at the center of the face
    .rect(length + 1, slot_width) # Make the rectangle slightly longer than block to ensure clean cut
    .cutThruAll()
)

# 3. Create the counterbored holes on the side face
# We select the front face (or side, depending on orientation). 
# Looking at the image, the holes are on the long side.
# Let's assume the long side is aligned with X. The holes are on the "front" face (e.g., -Y or +Y).
# Let's pick the +Y face (">Y").
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints([(-hole_spacing / 2.0, 0), (hole_spacing / 2.0, 0)]) # Center is (0,0) relative to the face center
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)

# Export or visualization would happen here normally, but the prompt asks for 'result' variable.