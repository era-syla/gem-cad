import cadquery as cq

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
panel_height = 600.0
panel_width = 300.0
panel_thickness = 30.0

# Groove configuration (dividing panel into 3 equal vertical sections)
groove_z_offset = panel_height / 6.0  # Distance from center for the two grooves
groove_opening_h = 10.0               # Height of groove at the surface
groove_base_h = 6.0                   # Height of groove at the bottom
groove_depth = 4.0                    # Depth of the cut

# Shiplap / Edge Step configuration
lap_width = 12.0
lap_thickness = panel_thickness / 2.0

# -----------------------------------------------------------------------------
# Modeling
# -----------------------------------------------------------------------------

# 1. Base Geometry
# Create the main rectangular block centered at the origin.
# Axis alignment: X = Width, Y = Thickness, Z = Height
result = cq.Workplane("XY").box(panel_width, panel_thickness, panel_height)

# 2. Edge Details (Shiplap Joint)
# To create an interlocking profile:
# - Right Edge (X+): Cut away the back half (Y-), leaving the front face visible.
# - Left Edge (X-): Cut away the front half (Y+), leaving a rear flange.
# This orientation matches the image where horizontal grooves (on front) extend to the right edge profile.

# Cutter for Right-Back corner
cutter_lap_rb = (
    cq.Workplane("XY")
    .box(lap_width, lap_thickness, panel_height)
    .translate((panel_width/2 - lap_width/2, -panel_thickness/2 + lap_thickness/2, 0))
)

# Cutter for Left-Front corner
cutter_lap_lf = (
    cq.Workplane("XY")
    .box(lap_width, lap_thickness, panel_height)
    .translate((-panel_width/2 + lap_width/2, panel_thickness/2 - lap_thickness/2, 0))
)

# Apply the edge cuts
result = result.cut(cutter_lap_rb).cut(cutter_lap_lf)

# 3. Horizontal Surface Grooves
# We define the cross-section of the groove on the YZ plane (Side View)
# and extrude it along the X axis to create a cutter tool.

# Coordinates for the trapezoidal groove profile on YZ plane:
# Local X corresponds to Global Y (Thickness)
# Local Y corresponds to Global Z (Height)
# We cut into the Front Face (Y = +thickness/2)
y_surf = panel_thickness / 2
y_btm = y_surf - groove_depth
z_outer = groove_opening_h / 2
z_inner = groove_base_h / 2

groove_profile_pts = [
    (y_surf + 5.0, z_outer),   # Start outside to ensure clean edge
    (y_surf, z_outer),         # Top edge at surface
    (y_btm, z_inner),          # Top edge at bottom
    (y_btm, -z_inner),         # Bottom edge at bottom
    (y_surf, -z_outer),        # Bottom edge at surface
    (y_surf + 5.0, -z_outer),  # End outside
    (y_surf + 5.0, z_outer)    # Close loop
]

# Create the solid cutter
groove_cutter = (
    cq.Workplane("YZ")
    .polyline(groove_profile_pts)
    .close()
    .extrude(panel_width * 1.5)        # Extrude wider than the panel width
    .translate((-panel_width * 0.75, 0, 0)) # Center along X axis
)

# Cut the grooves at the top and bottom positions
# Z=0 is the vertical center of the panel
result = result.cut(groove_cutter.translate((0, 0, groove_z_offset)))
result = result.cut(groove_cutter.translate((0, 0, -groove_z_offset)))