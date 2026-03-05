import cadquery as cq

# --- Dimensions & Parameters ---
thickness = 2.4  # Standard 3-ply pickguard thickness
neck_pocket_width = 56.0
neck_pocket_depth = 20.0
pocket_y_bottom = 50.0  # Y position of the bottom of the neck pocket
pocket_y_top = pocket_y_bottom + neck_pocket_depth
nw = neck_pocket_width / 2.0  # Half-width for symmetry calculations

# --- Geometry Definition ---

# Define key points for the outer contour (Counter-Clockwise visual trace)
# Starting from the bottom-right corner of the neck pocket
p_start = (nw, pocket_y_bottom)
p_neck_tr = (nw, pocket_y_top)
p_shoulder_r = (nw + 12, pocket_y_top)  # Right shoulder tip

# Right side curvature points
p_belly_r = (88, 15)       # Widest point on the right
p_cutout_start = (74, -30) # Start of the control plate cutout

# Control plate cutout (Concave arc area at bottom right)
p_cutout_mid = (62, -44)
p_cutout_end = (48, -50)

# Bottom and Lower Horn points
p_bottom_mid = (0, -42)
p_horn_tip = (-64, -68)    # Tip of the lower horn

# Left side curvature points
p_waist_l = (-48, -10)     # Narrowest waist point
p_bout_l = (-48, 40)       # Upper left curvature
p_shoulder_l = (-(nw + 12), pocket_y_top) # Left shoulder tip
p_neck_tl = (-nw, pocket_y_top)
p_neck_bl = (-nw, pocket_y_bottom)

# --- Generate Base Shape ---
# We use a mix of straight lines for the neck pocket area and splines for the organic body
pickguard_outline = (
    cq.Workplane("XY")
    .moveTo(p_start[0], p_start[1])
    .lineTo(p_neck_tr[0], p_neck_tr[1])
    .lineTo(p_shoulder_r[0], p_shoulder_r[1])
    
    # Large curve down the right side
    .spline([p_belly_r, p_cutout_start], includeCurrent=True)
    
    # Concave cutout for the control plate interface
    .threePointArc(p_cutout_mid, p_cutout_end)
    
    # Bottom curve swooping to the lower horn
    .spline([p_bottom_mid, p_horn_tip], includeCurrent=True)
    
    # Curve coming back up the left side (waist and upper bout)
    .spline([p_waist_l, p_bout_l, p_shoulder_l], includeCurrent=True)
    
    # Close the loop back around the neck pocket
    .lineTo(p_neck_tl[0], p_neck_tl[1])
    .lineTo(p_neck_bl[0], p_neck_bl[1])
    .close()
)

# Extrude the base plate
plate = pickguard_outline.extrude(thickness)

# --- Feature: Pickup Slot ---
# Create a slot for the neck pickup
slot_width = 70.0
slot_height = 16.0
slot_y_pos = 22.0  # Position relative to origin

pickup_cutout = (
    cq.Workplane("XY")
    .moveTo(0, slot_y_pos)
    .rect(slot_width, slot_height)
    .extrude(thickness)
    .edges("|Z") # Select vertical edges
    .fillet(slot_height / 2.0 - 0.01) # Round ends fully
)

# --- Feature: Mounting Holes ---
# Coordinates for screw holes based on visual estimation
hole_locations = [
    (nw + 6, pocket_y_top - 6),      # Top Right near neck
    (-(nw + 6), pocket_y_top - 6),   # Top Left near neck
    (-54, -58),                      # Bottom Left (Horn)
    (58, -40),                       # Bottom Right
    (81, 10),                        # Right Edge mid-belly
    (-42, 0),                        # Left Edge waist
]

# --- Final Assembly ---
result = (
    plate
    .cut(pickup_cutout)          # Cut the pickup slot
    .faces(">Z")                 # Select top face
    .workplane()
    .pushPoints(hole_locations)
    .hole(3.0)                   # Drill mounting holes (3mm dia)
)