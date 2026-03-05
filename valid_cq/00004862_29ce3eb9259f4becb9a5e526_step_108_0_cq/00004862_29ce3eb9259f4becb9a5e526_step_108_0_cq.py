import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
height = 80.0
leg_length_1 = 40.0
leg_length_2 = 40.0
thickness = 5.0

# Slot dimensions
slot_width = 8.0     # The diameter of the curved ends
slot_length = 15.0   # Center-to-center distance (or total length, usually center-to-center in slot function)
                     # Looking at the image, let's assume slot_length is the total length of the slot opening.
                     # CadQuery's slot2D takes length as tip-to-tip.

# Slot positioning
# It looks like there are two slots on each leg.
# Vertical positioning:
slot_vertical_spacing = 40.0 # Distance between top and bottom slots
slot_top_margin = 15.0       # Distance from top edge to center of top slot

# Horizontal positioning (centering on the leg face)
# The face width is leg_length - thickness (if measuring from the inside corner)
# Or just centered on the flat part of the leg.
leg_1_center_x = (leg_length_1 + thickness) / 2.0  # Center of the outer face relative to origin?
# Let's model it as an L-profile extrusion first, then cut slots.

# --- Modeling Strategy ---
# 1. Create an L-shaped profile sketch.
# 2. Extrude it to the height.
# 3. Create workplanes on the two outer faces.
# 4. Cut slots into those faces.

# --- Build the Main Body ---

# Create the L-shape base sketch
# We align the corner at the origin (0,0)
L_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_length_1, 0)
    .lineTo(leg_length_1, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, leg_length_2)
    .lineTo(0, leg_length_2)
    .close()
)

# Extrude to create the solid angle iron
bracket = L_profile.extrude(height)

# --- Cut Slots on Leg 1 (The leg along X-axis) ---

# Center of the face for Leg 1 (the one aligned with X)
# The face is on plane Y=0 (or slightly offset if we want to cut through).
# Center X is roughly (leg_length_1 + thickness)/2? No, visually it's centered on the flat area.
# Let's center it on the flange area: (leg_length_1 - thickness)/2 + thickness? 
# Usually, these are centered on the flange width. 
flange_width_1 = leg_length_1
slot_x_center_1 = flange_width_1 / 2.0 + thickness/2 # A rough guess to center it nicely

# Actually, a cleaner way is to select the face and work relative to it.
# Face normal is -Y.
bracket = (
    bracket.faces("<Y")
    .workplane(centerOption="CenterOfMass")
    .tag("face1")
)

# Calculate centers relative to the face center
# Face 1 dimensions: width = leg_length_1, height = height
# Center of face is at (leg_length_1/2, height/2) in global coords roughly.
# Let's define points relative to the center of the workplane.
# The slots seem vertically aligned.
y_offset = slot_vertical_spacing / 2.0

# Cut slots on Face 1
bracket = (
    bracket
    .pushPoints([(0, y_offset), (0, -y_offset)]) # Two vertical positions
    .slot2D(length=slot_length, diameter=slot_width, angle=90) # Vertical slots
    .cutThruAll()
)

# --- Cut Slots on Leg 2 (The leg along Y-axis) ---
# Face normal is -X.

bracket = (
    bracket.faces("<X")
    .workplane(centerOption="CenterOfMass")
)

# Cut slots on Face 2
bracket = (
    bracket
    .pushPoints([(0, y_offset), (0, -y_offset)])
    .slot2D(length=slot_length, diameter=slot_width, angle=90)
    .cutThruAll()
)

result = bracket