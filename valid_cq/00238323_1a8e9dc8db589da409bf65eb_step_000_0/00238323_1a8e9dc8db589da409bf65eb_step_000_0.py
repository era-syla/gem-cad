import cadquery as cq

# ---------------------------------------------------------
# Parametric Dimensions
# ---------------------------------------------------------
height = 110.0          # Total vertical height of the object
max_radius = 45.0       # Radius at the widest point of the body
top_radius = 35.0       # Radius at the top opening
thickness = 3.0         # Wall thickness

# ---------------------------------------------------------
# Geometry Construction
# ---------------------------------------------------------

# Define control points for the spline that forms the outer profile.
# The profile starts at (0,0), curves out to max_radius, and tapers to top_radius.
spline_points = [
    (25.0, 35.0),           # Lower body curvature point
    (max_radius, 75.0),     # Widest section (approx 2/3 up the height)
    (top_radius, height)    # End point at the top rim
]

# Create the 2D profile on the XZ plane
# We use a spline with specific tangents to control the shape:
# - Start tangent (1, 0): Horizontal tangent at bottom ensures a smooth round base
# - End tangent (0, 1): Vertical tangent at top ensures the rim is vertical
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .spline(spline_points, tangents=[(1, 0), (0, 1)])
    .lineTo(0, height)      # Draw line to the central axis at the top
    .lineTo(0, 0)           # Draw line down the central axis to close the loop
    .close()
)

# Revolve the profile 360 degrees around the Z-axis to create the solid form
# On the XZ plane, the default revolve axis is the local Y, which corresponds to global Z
solid_base = profile.revolve()

# Create the hollow vessel structure by shelling the solid
# We select the top face (highest Z) to be the opening
# A negative thickness value creates the walls inward
result = solid_base.faces(">Z").shell(-thickness)