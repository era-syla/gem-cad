import cadquery as cq

# --- Parameters ---
length = 32.0          # Length of the housing body
width = 20.0           # Overall width
height = 12.0          # Overall height
chamfer_w = 6.0        # Width of the polarizing chamfer cut
chamfer_h = 6.0        # Height of the polarizing chamfer cut
wall_thickness = 1.8   # Thickness of the housing walls
fillet_radius = 1.5    # Radius for body edges
pin_diameter = 2.5     # Diameter of the contact pins
pin_length = 5.0       # Protrusion length of the pins
pin_spacing_x = 5.0    # Horizontal spacing for pins
pin_spacing_y = 3.5    # Vertical spacing for pins

# --- Modeling ---

# 1. Create the Main Body Profile
# We sketch on the YZ plane. The profile is a rectangle with a chamfered corner
# on the bottom-right to match the polarized connector shape.
pts = [
    (-width/2, height/2),                         # Top-Left
    (width/2, height/2),                          # Top-Right
    (width/2, -height/2 + chamfer_h),             # Right side, start of chamfer
    (width/2 - chamfer_w, -height/2),             # Bottom side, end of chamfer
    (-width/2, -height/2)                         # Bottom-Left
]

# Extrude the profile to create the solid block
# We extrude along positive X
body = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# 2. Apply Fillets
# Smooth the longitudinal edges (along X axis)
# We filter edges that are along the X axis
body = body.edges("|X").fillet(fillet_radius)

# 3. Create the Internal Cavity (Shell)
# We select the face at X=0 (the "front") and shell inwards.
# A negative thickness removes material from the inside and removes the selected face.
body = body.faces("<X").shell(-wall_thickness)

# 4. Create the Pins
# Select the back face (>X) to draw pins.
# We arrange 3 pins in a triangular configuration (2 top, 1 bottom) which fits the profile.
pin_locs = [
    (-pin_spacing_x/2, pin_spacing_y/2),  # Top-Left Pin
    (pin_spacing_x/2, pin_spacing_y/2),   # Top-Right Pin
    (0, -pin_spacing_y/2)                 # Bottom Center Pin
]

pins = (
    body.faces(">X").workplane()
    .pushPoints(pin_locs)
    .circle(pin_diameter / 2)
    .extrude(pin_length)
)

# Combine pins with the main body
result = body.union(pins)

# 5. Detail the Pins
# Fillet the tips of the pins for a rounded contact appearance.
# We select edges at the very end of the X axis.
result = result.edges(">X").fillet(pin_diameter * 0.45)

# 6. Detail the Front Opening
# Add a small chamfer to the rim of the opening for better mating.
result = result.edges("<X").chamfer(wall_thickness * 0.2)