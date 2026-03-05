import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
main_diameter = 40.0
main_radius = main_diameter / 2.0
body_cyl_height = 45.0  # Height of the main cylindrical section
bottom_tip_height = 10.0 # Height of the bottom conical tip

# Top section dimensions
taper_height = 10.0     # Height of the conical transition
collar_diameter = 26.0  # Diameter of the section above the taper
collar_radius = collar_diameter / 2.0
collar_height = 5.0     # Height of the collar cylinder

neck_diameter = 18.0    # Diameter of the groove/neck
neck_radius = neck_diameter / 2.0
neck_height = 5.0       # Height of the neck

cap_diameter = 30.0     # Diameter of the top cap
cap_radius = cap_diameter / 2.0
cap_height = 8.0        # Height of the top cap

# --- Geometry Construction ---

# Calculate cumulative Z heights to define profile points
current_z = 0.0
z_tip = current_z + bottom_tip_height
z_body = z_tip + body_cyl_height
z_taper = z_body + taper_height
z_collar = z_taper + collar_height
z_neck = z_collar + neck_height
z_cap = z_neck + cap_height

# Define profile points for revolution (r, z) coordinates
# Drawing the right half of the profile on the XZ plane
profile_points = [
    (0, 0),                      # Bottom tip center
    (main_radius, z_tip),        # Top of bottom cone
    (main_radius, z_body),       # Top of main cylinder
    (collar_radius, z_taper),    # Top of taper
    (collar_radius, z_collar),   # Top of collar
    (neck_radius, z_collar),     # Bottom of neck (inward step)
    (neck_radius, z_neck),       # Top of neck
    (cap_radius, z_neck),        # Bottom of cap (outward step)
    (cap_radius, z_cap),         # Top of cap
    (0, z_cap)                   # Top center
]

# Create the solid by revolving the profile
# Using XZ plane, the local Y axis corresponds to the global Z axis
result = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve(axisStart=(0, 0, 0), axisEnd=(0, 1, 0))
)