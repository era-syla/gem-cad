import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
body_width = 12.0
body_length = 20.0
body_height = 10.0

# Flange (top plate) dimensions
flange_overhang = 2.0
flange_width = body_width + 2 * flange_overhang
flange_length = body_length + 2 * flange_overhang
flange_thickness = 2.0

# Rocker button dimensions
rocker_length = 12.0
rocker_width = 8.0
rocker_height_high = 3.0  # Height at the peak
rocker_height_low = 0.5   # Height at the base

# Pin/Terminal dimensions
pin_width = 0.8
pin_thickness = 4.0
pin_length = 6.0
pin_spacing = 6.0  # Distance between pin centers

# --- Construction ---

# 1. Main Housing Body
# Centered on XY plane, extending downwards in Z
housing = cq.Workplane("XY").box(body_length, body_width, body_height)

# 2. Top Flange
# Placed on top of the housing
flange = (
    cq.Workplane("XY")
    .workplane(offset=body_height / 2)
    .box(flange_length, flange_width, flange_thickness)
)

# 3. Rocker Button (Wedge shape)
# The rocker is a wedge. We can loft two rectangles or extrude a triangle.
# Let's extrude a triangle profile along the width.
rocker_profile = (
    cq.Workplane("XZ") # Drawing on Side view
    .workplane(offset=-rocker_width / 2) # Move to side of rocker
    .center(body_length / 4, body_height/2 + flange_thickness/2) # approximate position on top
    .moveTo(-rocker_length/2, 0)
    .lineTo(rocker_length/2, 0)
    .lineTo(rocker_length/2, rocker_height_high)
    .lineTo(-rocker_length/2, rocker_height_low)
    .close()
)

rocker = rocker_profile.extrude(rocker_width)

# 4. Connection Pins
# Create one pin and then pattern or copy it
# Pins extend downwards from the bottom of the housing
pin_plane = cq.Workplane("XY").workplane(offset=-body_height / 2)

# Create the center pin
center_pin = (
    pin_plane
    .box(pin_width, pin_thickness, pin_length, combine=False)
    .translate((0, 0, -pin_length / 2))
)

# Create the side pins
left_pin = center_pin.translate((-pin_spacing, 0, 0))
right_pin = center_pin.translate((pin_spacing, 0, 0))

# --- Assembly ---

result = (
    housing
    .union(flange)
    .union(rocker)
    .union(center_pin)
    .union(left_pin)
    .union(right_pin)
)

# Export or visualization would happen here, but only the result variable is required.