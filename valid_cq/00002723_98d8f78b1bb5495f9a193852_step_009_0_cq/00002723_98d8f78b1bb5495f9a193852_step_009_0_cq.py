import cadquery as cq

# --- Parametric Dimensions ---
# Main block dimensions
length = 50.0   # Total length along X
width = 30.0    # Total width along Y
height = 20.0   # Total height along Z
fillet_radius = 4.0 # Radius for the vertical corners

# Slot dimensions (the rectangular hole)
slot_width = 8.0   # Width of slot (Y)
slot_length = 15.0 # Length of slot (X)
slot_offset_x = -10.0 # Position relative to center (shifted left)

# T-slot / U-shape dimensions
u_stem_width = 8.0  # Width of the narrow part (Y)
u_stem_length = 10.0 # Length of the narrow part (X)
u_cross_width = 18.0 # Width of the wide part at the back (Y)
u_cross_length = 8.0 # Length of the wide part (X)
u_offset_x = 10.0    # Approximate center of the U-shape area

# --- Geometry Construction ---

# 1. Create the main base block
base = cq.Workplane("XY").box(length, width, height)

# 2. Apply fillets to the four vertical edges
result = base.edges("|Z").fillet(fillet_radius)

# 3. Cut the rectangular slot on the left side
# We select the top face to start drawing
result = result.faces(">Z").workplane() \
    .center(slot_offset_x, 0) \
    .rect(slot_length, slot_width) \
    .cutBlind(-height)

# 4. Cut the U-shaped feature on the right side
# We define the profile of the "U" or "T" cutout
# The shape consists of a wider rectangle connected to a narrower rectangle
# Or simply two overlapping rectangles cut out.

# Let's define the center for the right-side feature
right_feature_center_x = 10.0

# Cut the "cross bar" of the T/U shape (the wider part)
result = result.faces(">Z").workplane() \
    .center(right_feature_center_x + (u_cross_length/2), 0) \
    .rect(u_cross_length, u_cross_width) \
    .cutBlind(-height)

# Cut the "stem" of the T/U shape (the narrower connecting part)
# We position this so it connects the previous cut to the central area
result = result.faces(">Z").workplane() \
    .center(right_feature_center_x - (u_stem_length/2), 0) \
    .rect(u_stem_length, u_stem_width) \
    .cutBlind(-height)

# Alternatively, we could have drawn a custom polygon wire for the T-shape,
# but two rectangular cuts are robust and simple to parameterize.