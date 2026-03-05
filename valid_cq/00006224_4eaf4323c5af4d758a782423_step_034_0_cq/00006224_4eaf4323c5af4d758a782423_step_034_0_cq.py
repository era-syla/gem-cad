import cadquery as cq

# Parametric dimensions for the L-angle profile
length = 1000.0  # Total length of the angle bar
leg_width = 25.0 # Width of the horizontal leg
leg_height = 25.0 # Height of the vertical leg
thickness = 3.0  # Thickness of the material

# Create the L-shape cross-section
# We draw the L-shape on the YZ plane (or similar) and extrude along X
# Points are defined relative to an origin at the corner
pts = [
    (0, 0),
    (leg_width, 0),
    (leg_width, thickness),
    (thickness, thickness),
    (thickness, leg_height),
    (0, leg_height),
    (0, 0)
]

# Create the solid
result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# Optional: Center the beam if desired, but standard structural profiles
# are often origin-based at a corner. The current code starts extrusion 
# from the YZ plane at X=0 going towards positive X.