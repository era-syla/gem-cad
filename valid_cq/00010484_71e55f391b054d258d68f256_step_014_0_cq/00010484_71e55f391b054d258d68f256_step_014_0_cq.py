import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions based on visual estimation of common plastic housing proportions
total_length = 60.0    # Length along the main axis
total_width = 40.0     # The wider end
narrow_width = 25.0    # The narrower end
height = 10.0          # Thickness of the shell-like structure
wall_thickness = 2.0   # Thickness of the plastic walls

# Transition details
transition_start = 25.0 # Where the widening starts from the narrow end
transition_len = 10.0   # Length of the ramp/transition area

# Cutout details (T-shaped slots)
slot_width_top = 8.0
slot_height_top = 2.5
slot_width_stem = 2.5
slot_height_stem = 3.0
slot_spacing = 15.0     # Distance between the two slots
slot_x_offset = 12.0    # Distance from the narrow end edge

# Side cutout (the large open area on the left)
side_cutout_depth = 8.0
side_cutout_width = 20.0 # Approximate
tab_width = 5.0         # The small tabs remaining on the left

# Text details (approximation since actual text rendering depends on fonts)
text_string = "MODERN\nROBOTICS INC."
text_size = 4.0
text_depth = 0.5

# Fillets
outer_fillet = 2.0
edge_fillet = 1.0

# --- Geometry Construction ---

# 1. Base Shape: Create the main profile (top view silhouette) and extrude
# We'll create a sketch on the XY plane.
# The shape looks like a rectangle that widens.

def create_base_profile():
    pts = [
        (0, 0),
        (total_length, 0),
        (total_length, total_width),
        (transition_start + transition_len, total_width),
        (transition_start, narrow_width),
        (0, narrow_width)
    ]
    return cq.Workplane("XY").polyline(pts).close().extrude(height)

base_block = create_base_profile()

# 2. Shelling/Hollowing
# The object looks like a cover, so it's likely hollow underneath.
# We'll shell it, removing the bottom face (Z=0).
shelled = base_block.faces("<Z").shell(-wall_thickness)

# 3. Rounding Corners
# Apply fillets to the vertical edges to match the smooth look
# We need to select the outer vertical edges.
# The transition corners need specific handling to look like the image.
# Let's fillet the 4 main corners first, then the transition.

# Filter for vertical edges
vertical_edges = shelled.edges("|Z")
# We want the outer corners mostly.
shelled = shelled.edges("|Z").fillet(outer_fillet)

# 4. Top Face Fillet
# The top edge usually has a small cosmetic fillet
shelled = shelled.faces(">Z").edges().fillet(edge_fillet)


# 5. The T-Shaped Slots
# We need a custom profile for the T-slot.
def t_slot_sketch():
    # Center of the T is at local (0,0)
    w1, h1 = slot_width_top, slot_height_top
    w2, h2 = slot_width_stem, slot_height_stem
    
    # Points for a T shape
    # Top bar
    p1 = (-w1/2, h2 + h1)
    p2 = (w1/2, h2 + h1)
    p3 = (w1/2, h2)
    # Stem
    p4 = (w2/2, h2)
    p5 = (w2/2, 0)
    p6 = (-w2/2, 0)
    p7 = (-w2/2, h2)
    p8 = (-w1/2, h2)
    
    return cq.Sketch().polygon([p1, p2, p3, p4, p5, p6, p7, p8])

# Position the slots on the top face
# We need to calculate center points relative to the origin (0,0 of the main block)
# The narrow part is at X=0 to X=transition_start.
# Let's place them in the middle of the narrow section's width.
slot_y_center = narrow_width / 2.0
slot_x_1 = slot_x_offset
slot_x_2 = slot_x_offset + slot_spacing

# Create the cuts
result_with_slots = (
    shelled
    .faces(">Z")
    .workplane()
    .placeSketch(
        t_slot_sketch().moved(cq.Location(cq.Vector(slot_x_1, slot_y_center, 0))),
        t_slot_sketch().moved(cq.Location(cq.Vector(slot_x_2, slot_y_center, 0)))
    )
    .cutBlind(-height) # Cut through
)

# 6. Side Cutout (The large opening on the "left" / X=0 side in the image perspective)
# The image shows the side wall cut away, leaving two small tabs/hooks.
# This corresponds to the face at X=0 in our coordinate system, but likely cutting into the -Y side or similar.
# Looking at the image, the cutout is on the vertical face of the narrow section. 
# Based on the orientation, let's assume the "narrow_width" side (Y axis in our code) is the vertical face shown.
# Actually, re-orienting based on standard CAD views:
# Let's assume the flat face with slots is Top (XY).
# The "left" side in the image is the X=0 face.
# The cutout removes material from the X=0 face, creating the "C" shaped profile.

# Define the cutout rectangle
cutout_height = narrow_width - (2 * tab_width) # Leaving tabs on ends
cutout_center_y = narrow_width / 2.0

# It seems the cutout goes through the wall on the X=0 face.
# Let's cut a rectangle out of that face.
final_shape = (
    result_with_slots
    .faces("<X")
    .workplane()
    .center(0, 0) # Center on the face
    # We shift Y because the face center might not align with our desired cutout center perfectly if not symmetric
    # But here the face is centered at Y = narrow_width/2, Z = height/2
    .rect(cutout_height, height * 2) # Width (along Y), Height (along Z). Oversize Z to clear.
    .cutBlind(-side_cutout_depth) 
)

# 7. Text "MODERN ROBOTICS INC."
# The text is on the wider section.
# Orientation: Rotated 90 degrees or running along the Y axis?
# In the image, "MODERN" is closer to the transition, "ROBOTICS INC" below it.
# Text runs parallel to the Y axis (width).

text_center_x = transition_start + transition_len + (total_length - (transition_start + transition_len))/2
text_center_y = total_width / 2.0

# We need to construct the text on the top face.
# Note: Complex fonts can be slow or fail in kernels depending on system installation.
# We will use a simple geometric approximation or standard font if available.
try:
    final_shape = (
        final_shape
        .faces(">Z")
        .workplane()
        .center(text_center_x, text_center_y)
        .transformed(rotate=(0, 0, -90)) # Rotate text alignment
        .text("MODERN", text_size, text_depth, cut=True, combine=True)
        .center(0, -text_size * 1.5) # Move down for second line
        .text("ROBOTICS INC.", text_size, text_depth, cut=True, combine=True)
    )
except Exception:
    # Fallback if text generation fails (common in some headless CI environments)
    # Just make a small pocket to represent text area
    final_shape = (
        final_shape
        .faces(">Z")
        .workplane()
        .center(text_center_x, text_center_y)
        .rect(total_width - 10, 10)
        .cutBlind(-0.2)
    )

result = final_shape