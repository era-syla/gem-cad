import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
main_diameter = 20.0
main_height = 30.0

# Bottom tip dimensions
tip_height = 5.0

# Neck and shoulder transition dimensions
shoulder_height = 3.0  # Height of the tapered transition
neck_diameter = 11.0
neck_height = 4.0

# Top cap/head dimensions
head_diameter = 16.0
head_height = 4.0

# --- Geometry Construction ---
# Calculate radii and Z-stack coordinates
r_main = main_diameter / 2.0
r_neck = neck_diameter / 2.0
r_head = head_diameter / 2.0

z0 = 0.0
z1 = z0 + tip_height
z2 = z1 + main_height
z3 = z2 + shoulder_height
z4 = z3 + neck_height
z5 = z4 + head_height

# Define the profile points for revolution in the XZ plane.
# The profile represents the right half of the cross-section.
# Format: (Radius, Z-Height)
profile_points = [
    (0, z0),              # Bottom tip center
    (r_main, z1),         # End of tip cone / Bottom of main body
    (r_main, z2),         # Top of main body / Start of shoulder taper
    (r_neck, z3),         # Top of shoulder / Bottom of neck
    (r_neck, z4),         # Top of neck / Underside of head
    (r_head, z4),         # Head overhang outer edge
    (r_head, z5),         # Top of head outer edge
    (0, z5)               # Top center
]

# Create the solid by revolving the profile around the Z-axis
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve()
)