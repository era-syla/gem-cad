import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
length = 100.0  # Total length of the main bar
height = 20.0   # Height of the bar
thickness = 5.0 # Thickness of the material
arm_length = 15.0 # Length of the perpendicular arms at the ends

# Notch dimensions (top edge)
notch_width = 5.0
notch_depth = 5.0

# Slot dimensions (rectangular holes)
slot_width = 4.0
slot_height = 8.0
slot_y_pos = -2.0 # Vertical offset from center or specific Y position

# Distance from ends for features
feature_offset = 20.0 # Distance from the center to the notches/slots

# --- Modeling Process ---

# 1. Create the base "U" shape profile
# We will draw the top-down profile and extrude it upwards.
# Alternatively, we can draw the front face and extrude, then add arms.
# Let's try drawing the top-down U-shape profile and extruding to height.

# Calculate points for the U-shape path
# We'll center the main beam on the X axis.
half_length = length / 2.0
pts = [
    (half_length, 0),
    (half_length, arm_length),
    (half_length - thickness, arm_length),
    (half_length - thickness, thickness),
    (-(half_length - thickness), thickness),
    (-(half_length - thickness), arm_length),
    (-half_length, arm_length),
    (-half_length, 0)
]

# Create the base extrusion
base = (
    cq.Workplane("XZ") # Drawing on ground plane, extruding up Y (height)
    .polyline(pts)
    .close()
    .extrude(height)
)

# 2. Add Top Notches
# We need notches on the top edge of the main beam.
# Located symmetrically from the center.
notch_locations = [
    (feature_offset, height), 
    (-feature_offset, height)
]

# We need to cut these from the "top" face relative to the original sketch, 
# but since we extruded in Y, the top is at y=height.
# Let's select the main back face or front face to cut through.
# Actually, selecting the top face and cutting down is easiest.

result = (
    base
    .faces(">Y") # Select top face
    .workplane()
    .center(0, thickness/2.0) # Move workplane center to align with the main beam thickness
    .pushPoints([(feature_offset, 0), (-feature_offset, 0)])
    .rect(notch_width, thickness + 2.0) # Make rectangle slightly wider than thickness to ensure cut
    .cutBlind(-notch_depth)
)

# 3. Add Rectangular Slots/Holes
# These are on the main face (front face of the beam).
# We need to position them below the notches typically.

result = (
    result
    .faces(">Z") # Select the front face of the main beam
    .workplane()
    .pushPoints([(feature_offset, slot_y_pos), (-feature_offset, slot_y_pos)])
    .rect(slot_width, slot_height)
    .cutBlind(-thickness * 2) # Cut through
)

# 4. Add the center notch (optional interpretation)
# Looking closely at the image, there seems to be a wider, shallow cutout 
# or just a visual artifact in the very center top edge. 
# It looks like a wider, shallower notch in the middle. Let's add it.
center_notch_width = 15.0
center_notch_depth = 2.0

result = (
    result
    .faces(">Y")
    .workplane()
    .center(0, thickness/2.0)
    .rect(center_notch_width, thickness + 2.0)
    .cutBlind(-center_notch_depth)
)

# Export or Show (commented out for script usage, 'result' is the key variable)
# show_object(result)