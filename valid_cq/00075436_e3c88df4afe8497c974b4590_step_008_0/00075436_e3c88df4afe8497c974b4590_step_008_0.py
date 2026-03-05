import cadquery as cq

# -- Parametric Dimensions --
# Main body dimensions
body_radius = 15.0
body_height = 40.0

# Bottom tip dimensions
tip_height = 5.0

# Top section dimensions
shoulder_height = 4.0   # Height of the conical transition
neck_radius = 8.5       # Radius of the narrow neck
neck_height = 5.0       # Height of the vertical neck section
cap_radius = 13.0       # Radius of the top button/cap
cap_height = 5.0        # Thickness of the top cap

# -- Profile Calculation --
# Calculate vertical (Z) coordinates for each section
z0 = 0.0
z1 = z0 + tip_height
z2 = z1 + body_height
z3 = z2 + shoulder_height
z4 = z3 + neck_height
z5 = z4 + cap_height

# Define the points for the profile to revolve
# Drawn on the XZ plane: X corresponds to radius, Z (local Y) corresponds to height
profile_points = [
    (0, z0),                    # Bottom tip (Center)
    (body_radius, z1),          # Base of bottom cone / Start of body
    (body_radius, z2),          # Top of main body
    (neck_radius, z3),          # Top of shoulder / Start of neck
    (neck_radius, z4),          # Top of neck
    (cap_radius, z4),           # Bottom outer edge of cap (overhang)
    (cap_radius, z5),           # Top outer edge of cap
    (0, z5)                     # Top center
]

# -- Model Generation --
# Create the solid by revolving the profile around the Z-axis (local Y of XZ plane)
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)