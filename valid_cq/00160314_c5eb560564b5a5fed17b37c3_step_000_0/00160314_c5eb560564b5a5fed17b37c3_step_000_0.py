import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
base_radius = 28.0
neck_radius = 11.0
body_height = 65.0

# Cap/Stopper dimensions
flare_height = 5.0        # Height of the transition from neck to cap
lower_rim_radius = 14.0   # Radius of the lower ring of the cap
lower_rim_height = 3.5    # Height of the lower ring
groove_radius = 11.5      # Radius of the groove indentation
groove_height = 3.0       # Height of the groove
top_cap_radius = 16.0     # Radius of the very top disc
top_cap_height = 5.0      # Thickness of the top disc

# Calculate vertical (Z) coordinates for each section
z_base = 0
z_neck_start = body_height
z_flare_top = z_neck_start + flare_height
z_rim_top = z_flare_top + lower_rim_height
z_groove_top = z_rim_top + groove_height
z_top = z_groove_top + top_cap_height

# --- Geometry Construction ---

# Define the profile on the XZ plane to be revolved around the Z axis.
# The profile consists of the base, the organic body curve, and the technical cap details.

result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    
    # Create the main "bell" shape using a spline.
    # We define intermediate control points to shape the curve.
    # Tangents [(0, 1), (0, 1)] ensure the curve is vertical at the base and neck,
    # creating a smooth transition.
    .spline(
        [
            (base_radius * 0.95, body_height * 0.2), 
            (base_radius * 0.60, body_height * 0.55), 
            (neck_radius, z_neck_start)
        ],
        includeCurrent=True,
        tangents=[(0, 1.0), (0, 1.0)]
    )
    
    # 1. Flared transition from neck to the cap assembly
    .lineTo(lower_rim_radius, z_flare_top)
    
    # 2. Vertical face of the lower rim
    .lineTo(lower_rim_radius, z_rim_top)
    
    # 3. The Groove (Horizontal in, Vertical up, Horizontal out)
    .lineTo(groove_radius, z_rim_top)      # Inward
    .lineTo(groove_radius, z_groove_top)   # Up
    .lineTo(top_cap_radius, z_groove_top)  # Outward to top cap radius
    
    # 4. Vertical face of the top cap
    .lineTo(top_cap_radius, z_top)
    
    # 5. Top face closing to the center axis
    .lineTo(0, z_top)
    
    # Close the profile back to origin to form a valid face
    .close()
    
    # Create the solid by revolving the profile 360 degrees around the Z axis
    .revolve()
)