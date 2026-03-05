import cadquery as cq

# Define parametric variables for dimensions
plate_thickness = 3.0
fillet_radius = 2.0
corner_fillet = 5.0
nose_fillet = 10.0

# Approximate dimensions based on the visual proportions
# The shape is roughly symmetric about the centerline, but slightly asymmetric in the rear.
# We will model the main outline using points and lines.

# Coordinates for the main outline (x, y) starting from the nose (top right in image)
# Assuming the nose tip is at some positive X. Let's orient length along X.
# Let's start sketching from the "nose" tip and go counter-clockwise.

pts = [
    (80, 0),       # Nose tip
    (75, 20),      # Front upper edge start
    (75, 25),      # First notch start
    (65, 25),      # First notch inner
    (65, 35),      # Second notch start
    (45, 35),      # Second notch inner
    (45, 45),      # Third notch start (main body width start)
    (-10, 45),     # Upper rear corner
    (-25, 30),     # Upper rear slant
    (-50, 25),     # Rear "tail" start
    (-50, 15),     # Rear tail upper notch
    (-60, 15),     # Rear tail end top
    (-60, -15),    # Rear tail end bottom
    (-50, -15),    # Rear tail lower notch
    (-50, -25),    # Rear tail lower start
    (-30, -35),    # Lower rear slant
    (0, -45),      # Lower rear corner
    (50, -45),     # Lower main body end
    (55, -35),     # Lower notch vertical
    (65, -35),     # Lower notch horizontal
    (65, -20),     # Front lower edge start
    (80, 0)        # Back to nose tip
]

# Hole positions (x, y) estimates
hole_positions = [
    (40, 30),
    (60, 15),
    (70, -10),
    (30, -30),
    (-10, -30),
    (-30, 0),
    (-45, 10),
    (-45, -10),
    (30, 0)
]
hole_diameter = 3.0

# Build the main geometry
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(plate_thickness)
)

# Apply fillets to sharp exterior corners for a smoother look
# We select edges along the Z axis
result = result.edges("|Z").fillet(fillet_radius)

# Create the holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)