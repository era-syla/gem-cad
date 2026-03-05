import cadquery as cq

# Parametric dimensions based on visual estimation of the image
width = 180.0
height_right = 130.0
height_left = 75.0
peak_x = 80.0    # X-coordinate of the top peak
peak_y = 155.0   # Y-coordinate of the top peak
thickness = 3.0
fillet_radius = 2.0

# Hole specifications (Countersunk M3/M4 style)
hole_diameter = 3.5
csk_diameter = 7.0
csk_angle = 90.0

# Hole coordinates [(x, y), ...]
hole_locations = [
    (12, 25),             # Left edge, lower
    (12, 60),             # Left edge, upper
    (55, 12),             # Bottom edge, left
    (width - 55, 12),     # Bottom edge, right
    (width - 12, 25),     # Right edge, lower
    (width - 12, 105)     # Right edge, upper
]

# Define the polygon vertices starting from bottom-left
points = [
    (0, 0),
    (width, 0),
    (width, height_right),
    (peak_x, peak_y),
    (0, height_left)
]

# Create the base geometry
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

# Apply fillets to the vertical profile corners
result = result.edges("|Z").fillet(fillet_radius)

# Add countersunk holes on the top face
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)