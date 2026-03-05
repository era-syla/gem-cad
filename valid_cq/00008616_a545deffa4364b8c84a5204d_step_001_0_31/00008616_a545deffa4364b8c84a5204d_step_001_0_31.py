import cadquery as cq

# Define coordinates for the outline of Texas
# Mapped approximately proportionally to latitude/longitude
pts = [
    (-30, 65),   # NW Panhandle (36.5 N, 103 W)
    (0, 65),     # NE Panhandle (36.5 N, 100 W)
    (0, 45),     # Panhandle East / Red River start
    (8, 43),     # Red River points...
    (15, 45),
    (25, 41),
    (35, 42),
    (45, 38),
    (55, 36),
    (60, 35),    # NE Corner (Texarkana)
    (60, 15),    # Louisiana Border straight section
    (63, 10),    # Sabine River points...
    (61, 7),
    (66, 3),
    (60, -5),    # Sabine Mouth
    (50, -10),   # Gulf Coast points...
    (40, -16),
    (30, -25),
    (28, -32),
    (25, -40),   # Brownsville (South Tip)
    (15, -32),   # Rio Grande points...
    (8, -28),
    (2, -20),
    (-5, -10),
    (-10, -5),   # Del Rio area
    (-18, -12),  # Big Bend starts
    (-25, -24),  # Big Bend deep south
    (-32, -26),  
    (-38, -10),  # Big Bend west
    (-45, -2),
    (-52, 5),
    (-58, 12),
    (-65, 18),   # El Paso (West Tip)
    (-65, 20),   # New Mexico Border South
    (-30, 20)    # New Mexico Border Corner
]

# Set the extrusion thickness
thickness = 10.0

# Create the 3D model by drawing the polygon and extruding
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)