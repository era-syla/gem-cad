import cadquery as cq

# Parametric dimensions for the L-angle beam
length = 400.0       # Total extrusion length
leg_width = 30.0     # Width of the horizontal leg
leg_height = 30.0    # Height of the vertical leg
thickness = 3.0      # Material thickness

# Define the coordinates for the L-shaped cross-section
# Starting from the outer corner at (0,0)
profile_pts = [
    (0, 0),
    (leg_width, 0),
    (leg_width, thickness),
    (thickness, thickness),
    (thickness, leg_height),
    (0, leg_height),
    (0, 0)
]

# Generate the 3D geometry
result = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .extrude(length)
)