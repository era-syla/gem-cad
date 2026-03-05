import cadquery as cq

# Parametric dimensions based on visual analysis
length = 200.0      # Total length of the plank
width = 50.0        # Total width of the top surface
height = 10.0       # Total height/thickness
flange_height = 4.0 # Thickness of the top wider section
base_width = 42.0   # Width of the narrower bottom section (creating the side steps)
seam_width = 0.5    # Width of the cosmetic groove in the center
seam_depth = 1.0    # Depth of the cosmetic groove

# Calculate coordinates for the cross-section profile
# The profile is sketched on the YZ plane, centered at (0,0)
y_outer = width / 2.0
y_inner = base_width / 2.0
z_top = height / 2.0
z_shelf = z_top - flange_height
z_bottom = -height / 2.0

# Define the points for the stepped profile (clockwise starting from top-right)
profile_points = [
    (y_outer, z_top),     # Top-right corner
    (y_outer, z_shelf),   # Drop down to shelf
    (y_inner, z_shelf),   # Move inward along shelf
    (y_inner, z_bottom),  # Drop to bottom
    (-y_inner, z_bottom), # Move across bottom
    (-y_inner, z_shelf),  # Move up to shelf
    (-y_outer, z_shelf),  # Move outward along shelf
    (-y_outer, z_top),    # Move up to top-left corner
]

# Generate the main geometry
# 1. Sketch profile on YZ plane
# 2. Extrude symmetrically along X axis
result = (
    cq.Workplane("YZ")
    .polyline(profile_points)
    .close()
    .extrude(length / 2.0, both=True)
)

# Add the central dividing groove
# 1. Select the top face (+Z)
# 2. Create a workplane
# 3. Draw a rectangle spanning the width (Y) and the seam width (X)
# 4. Cut into the part
result = (
    result.faces(">Z")
    .workplane()
    .rect(seam_width, width * 1.1)  # Width slightly larger than part width to ensure clean cut
    .cutBlind(-seam_depth)
)