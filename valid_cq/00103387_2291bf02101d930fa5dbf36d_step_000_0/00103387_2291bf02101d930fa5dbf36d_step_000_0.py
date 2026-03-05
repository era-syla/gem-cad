import cadquery as cq

# --- Parametric Dimensions ---
# Dimensions approximated based on standard rifle cartridges (e.g., 7.62mm style)
# All units in millimeters

# Base and Rim
base_diameter = 12.0
base_radius = base_diameter / 2.0
rim_height = 1.5
chamfer_base = 0.5

# Extractor Groove
groove_diameter = 10.4
groove_radius = groove_diameter / 2.0
groove_width = 1.8
# The vertical space occupied by the angled cuts into the groove
groove_transition = 0.5 

# Main Body
body_start_height = rim_height + groove_transition + groove_width + groove_transition
body_diameter_start = 11.9
body_radius_start = body_diameter_start / 2.0
body_diameter_end = 11.4  # Slight taper towards shoulder
body_radius_end = body_diameter_end / 2.0
shoulder_start_height = 37.0

# Shoulder
shoulder_height = 4.0
shoulder_end_height = shoulder_start_height + shoulder_height
neck_diameter = 8.6
neck_radius = neck_diameter / 2.0

# Neck
neck_length = 7.0
case_mouth_height = shoulder_end_height + neck_length

# Bullet (Projectile)
bullet_diameter = 7.82  # Standard .30 caliber
bullet_radius = bullet_diameter / 2.0
total_height = 68.0

# --- Geometry Construction ---

# We define the half-profile of the cartridge on the XZ plane.
# X corresponds to the radius, Y corresponds to the height (Global Z).
# The profile is then revolved around the vertical axis.

result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    # Bottom Base with small chamfer
    .lineTo(base_radius - chamfer_base, 0)
    .lineTo(base_radius, chamfer_base)
    # Rim Edge
    .lineTo(base_radius, rim_height)
    # Extractor Groove: Angled cut in -> Straight -> Angled cut out
    .lineTo(groove_radius, rim_height + groove_transition)
    .lineTo(groove_radius, rim_height + groove_transition + groove_width)
    .lineTo(body_radius_start, body_start_height)
    # Main Case Body (Tapered Cylinder)
    .lineTo(body_radius_end, shoulder_start_height)
    # Shoulder (Conical Taper)
    .lineTo(neck_radius, shoulder_end_height)
    # Neck (Cylinder)
    .lineTo(neck_radius, case_mouth_height)
    # Step in for Bullet (Visualizes the seam between case and projectile)
    .lineTo(bullet_radius, case_mouth_height)
    # Bullet Ogive (Aerodynamic curve to the tip)
    # Using a spline to create a tangent ogive shape
    # Start tangent is vertical (0, 1), End tangent points slightly in (-0.2, 1)
    .spline(
        [(0, total_height)], 
        tangents=[(0, 5), (-0.5, 5)], 
        includeCurrent=True
    )
    # Close the profile back to the center axis
    .close()
    # Revolve 360 degrees around the Z-axis (Local Y of XZ plane)
    .revolve(360, (0, 0, 0), (0, 1, 0))
)