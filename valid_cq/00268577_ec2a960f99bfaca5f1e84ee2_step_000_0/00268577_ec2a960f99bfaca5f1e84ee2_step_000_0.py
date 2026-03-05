import cadquery as cq

# Parametric dimensions
body_radius = 5.0
body_height = 30.0
nose_height = 10.0

fin_width = 8.0       # Distance extending from the fuselage
fin_height = 12.0     # Height of the fin along the fuselage
fin_thickness = 1.0   # Thickness of the fin material
num_fins = 4

# 1. Create the Main Hull (Cylinder Body + Nose Cone)
# Using a revolve operation allows creating the main body and nose cone
# as a single continuous solid, while preserving the sharp transition edge.
hull_profile_pts = [
    (0, 0),                                 # Bottom center
    (body_radius, 0),                       # Bottom edge
    (body_radius, body_height),             # Shoulder (cylinder top)
    (0, body_height + nose_height)          # Nose tip
]

hull = (
    cq.Workplane("XZ")
    .polyline(hull_profile_pts)
    .close()
    .revolve(360)
)

# 2. Create a Single Fin
# Draw the triangular profile on the XZ plane and extrude it.
# We embed the fin slightly into the body to ensure a clean boolean union.
embed_depth = 0.5
fin_pts = [
    (body_radius - embed_depth, 0),           # Bottom inner corner (embedded)
    (body_radius + fin_width, 0),             # Bottom outer corner
    (body_radius - embed_depth, fin_height)   # Top inner corner (embedded)
]

fin = (
    cq.Workplane("XZ")
    .polyline(fin_pts)
    .close()
    .extrude(fin_thickness / 2.0, both=True)  # Symmetric extrusion
)

# 3. Pattern and Combine
# Start with the main hull and union the fins rotated around the Z-axis.
result = hull

for i in range(num_fins):
    angle = i * (360.0 / num_fins)
    # Rotate the fin instance around the Z-axis (0,0,0) to (0,0,1)
    rotated_fin = fin.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated_fin)