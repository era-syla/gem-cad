import cadquery as cq

# Parameters for the tapered plate model
length = 120.0
width_wide = 35.0
width_narrow = 15.0
thickness = 4.0
corner_radius = 5.0
edge_fillet_radius = 1.2

# Define the vertices for the trapezoidal shape
# Oriented with the wide end at negative X and narrow end at positive X
points = [
    (-length / 2, width_wide / 2),
    (length / 2, width_narrow / 2),
    (length / 2, -width_narrow / 2),
    (-length / 2, -width_wide / 2)
]

# Create the base solid
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

# Apply fillets to creating the rounded shape
# 1. Fillet the vertical corners (plan view shape)
result = result.edges("|Z").fillet(corner_radius)

# 2. Fillet the top and bottom face edges (smooth edges)
result = result.faces(">Z or <Z").edges().fillet(edge_fillet_radius)