import cadquery as cq

# --- Parameters ---
# Overall dimensions of the panel
panel_height = 100.0
panel_width = 80.0
panel_thickness = 5.0

# Dimensions for the edge features (step/rabbet profile)
# The image shows a stepped edge on the right side.
# Let's assume a simple rabbet joint or lap joint profile.
step_width = 2.0   # Width of the cutout
step_depth = 2.5   # Depth into the thickness (half thickness is a common choice)
# The image shows a notch near the top edge on the side profile as well.
# Actually, looking closer, it looks like a continuous profile along the vertical edge.
# The right edge has a 'lip' protruding from the back face, or a recess on the front face.
# Let's interpret this as a simple rabbet along the entire vertical edge.

# However, looking extremely closely at the top right corner, there is a small notch cut out
# horizontally as well, or perhaps it's just the profile.
# It looks like a classic tongue-and-groove siding profile or a lap joint.
# The right edge has a recess.
# Let's model a rectangular board with a simple rabbet cut on one vertical edge.

rabbet_width = 3.0    # How far the cut goes into the width of the board
rabbet_depth = panel_thickness / 2.0  # How deep the cut is into the thickness

# --- Modeling ---

# 1. Create the main base plate
# Centered on XY for convenience
result = cq.Workplane("XY").box(panel_width, panel_height, panel_thickness)

# 2. Create the cutout (rabbet) on the right edge
# We need to select the appropriate face/edge to cut.
# The box is centered, so x extends from -width/2 to +width/2.
# We want to cut along the edge at x = +width/2.
# The cut will be a rectangular prism subtracted from the main body.

# Calculate position for the cutter
# We want to cut into the front face (Z positive) or back face (Z negative)?
# The image shows the main face grey and flat. The right edge shows a step down.
# This implies the front face is wider than the back face (if the step is on the back)
# OR the front face is narrower (if the step is on the front).
# Let's assume the step removes material from the front-right corner.

cutter_x_pos = (panel_width / 2) - (rabbet_width / 2)
# The cutter needs to align with the edge, so its center is shifted.
# If cutter width is rabbet_width * 2 (to be safe), we position it so it cuts exactly rabbet_width in.
# Easier method: Workplane based.

# Select the front face (Z max)
result = (
    result
    .faces(">Z") 
    .workplane()
    # Move to the right edge
    .center(panel_width / 2, 0) 
    # Draw a rectangle to cut. 
    # Dimensions: rabbet_width wide (going inwards), panel_height tall.
    # Since we centered on the edge, we draw a rectangle that overlaps the corner.
    .rect(rabbet_width * 2, panel_height) 
    .cutBlind(-rabbet_depth)
)

# Optional: The image has a very specific "notch" look near the top of that edge profile.
# It looks like a standard shiplap or tongue/groove profile. 
# But without more detail, a simple rabbet (lap joint) is the most faithful geometric interpretation 
# of the primary visible feature: a step on the vertical edge.

# If we look really closely at the top right corner of the provided image, 
# there is a small horizontal cut into the "tongue".
# This suggests a more complex profile than just a simple rabbet. 
# It looks like a groove. Let's add a small groove to the vertical edge.

groove_width = 1.0
groove_depth = 1.0
groove_z_offset = -rabbet_depth / 2 # Positioned within the stepped area

# Let's refine the model to match a "grooved" edge which is common in cladding panels.
# Let's assume the basic L-shape cut we just made, plus a small notch.
# Actually, looking at the crop, it's just a simple L-profile (rabbet) running vertically.
# The "notch" appearance might just be an artifact of the rendering lines or a small chamfer.
# I will stick to the single vertical rabbet as it's the dominant feature.

# Final cleanup or specific orientation if needed.
# The image shows the panel standing up.
result = result.rotate((0,0,0), (1,0,0), 90)

# Export or returning for display
# (The 'result' variable is already set)