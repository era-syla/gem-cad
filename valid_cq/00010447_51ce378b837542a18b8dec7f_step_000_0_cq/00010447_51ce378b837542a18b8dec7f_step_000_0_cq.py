import cadquery as cq

# --- Parameters ---

# Main Body dimensions
body_width = 12.0
body_depth = 20.0
body_height = 15.0

# Top Flange dimensions
flange_width = 15.0
flange_depth = 25.0
flange_thickness = 2.0

# Actuator (Rocker) dimensions
rocker_width = 10.0
rocker_depth = 14.0
rocker_height_low = 0.5
rocker_height_high = 5.0
rocker_offset_y = 3.0  # Shift the rocker slightly towards one end

# Pin dimensions
pin_width = 0.8
pin_depth = 4.0
pin_length = 6.0
pin_spacing = 7.0  # Distance between centers of outer pins
pin_count = 3

# --- Modeling ---

# 1. Main Housing Body
# Centered on XY, extending downwards from Z=0 for convenience, or upwards.
# Let's build upwards from Z=0.
housing = cq.Workplane("XY").box(body_width, body_depth, body_height)

# 2. Top Flange
# Placed on top of the main body
flange = (
    cq.Workplane("XY")
    .workplane(offset=body_height / 2 + flange_thickness / 2)
    .box(flange_width, flange_depth, flange_thickness)
)

# 3. The Rocker Actuator (Wedge shape)
# We need to create a wedge. We can sketch a triangle on the side and extrude it
# or use a loft or a custom vertex construction. Extruding a side profile is usually easiest.
# Let's locate the sketch plane on the side of where the rocker sits.

# Calculate the Z level for the base of the rocker
rocker_base_z = body_height / 2 + flange_thickness

# Create the profile for the wedge
# Looking from the side (YZ plane equivalent), it goes from low to high.
rocker_profile = (
    cq.Workplane("YZ")
    .workplane(offset=rocker_base_z) # Move sketch plane to top of flange
    .center(0, rocker_offset_y)      # Position relative to center
    .moveTo(-rocker_depth / 2, 0)
    .lineTo(-rocker_depth / 2, rocker_height_low)
    .lineTo(rocker_depth / 2, rocker_height_high)
    .lineTo(rocker_depth / 2, 0)
    .close()
)

# Extrude the profile to create the width
rocker = rocker_profile.extrude(rocker_width, both=True)
# Note: The 'YZ' plane creates an X-axis extrusion. Since we want width along X, 
# but the profile was drawn on YZ (where horizontal is Y, vertical is Z in local coords),
# standard extrusion goes along global X.

# We need to rotate/orient the sketch correctly. The previous logic was slightly off.
# Let's retry the rocker sketch on the XZ plane to get the slope along Y.
rocker_profile_xz = (
    cq.Workplane("YZ")
    .workplane(offset=0) # Center X
    .center(rocker_offset_y, rocker_base_z) # Move Y center, and up to Z level
    # Draw shape in Y-Z coordinates of the global space
    .moveTo(-rocker_depth/2, 0) 
    .lineTo(rocker_depth/2, 0)
    .lineTo(rocker_depth/2, rocker_height_high)
    .lineTo(-rocker_depth/2, rocker_height_low)
    .close()
)
# Extrude symmetrically along X
rocker = rocker_profile_xz.extrude(rocker_width/2.0, both=True)


# 4. Pins
# We need 3 pins extending downwards from the bottom of the housing.
pin_z_start = -body_height / 2

def create_pin(offset_y):
    return (
        cq.Workplane("XY")
        .workplane(offset=pin_z_start - pin_length / 2)
        .center(0, offset_y)
        .box(pin_width, pin_depth, pin_length)
    )

pins = create_pin(0) # Center pin
pins = pins.union(create_pin(pin_spacing)) # Top/Back pin
pins = pins.union(create_pin(-pin_spacing)) # Bottom/Front pin


# --- Combine All Parts ---

result = housing.union(flange).union(rocker).union(pins)

# Optional: Add small fillets or chamfers to make it look realistic?
# The image shows sharp edges mostly, so we leave it sharp.