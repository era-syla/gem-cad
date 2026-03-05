import cadquery as cq

# Parametric dimensions
L_narrow = 50.0       # Length of the narrow section (left)
L_wide = 40.0         # Length of the wide section (right)
W_narrow = 30.0       # Width of the narrow section
W_wide = 50.0         # Width of the wide section
T_plate = 5.0         # Thickness of the top plate
T_web = 10.0          # Thickness (width) of the vertical rib
H_web = 10.0          # Height of the vertical rib (protrusion downwards)
R_fillet = 5.0        # Fillet radius for plate corners

# Calculate total length
L_total = L_narrow + L_wide

# 1. Create the Top Plate
# Define the profile points counter-clockwise starting from (0,0)
# (0,0) is the bottom-left corner of the narrow section.
# The bottom edge (y=0) is straight. The step is on the top edge.
pts = [
    (0, 0),
    (L_total, 0),
    (L_total, W_wide),
    (L_narrow, W_wide),
    (L_narrow, W_narrow),
    (0, W_narrow)
]

plate = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(T_plate)
)

# Apply fillets to the outer corners
# We select vertical edges (|Z) but exclude the edges at the step transition (x = L_narrow)
# to keep the internal and external step corners sharp, matching a machined look.
# The filter selects edges whose center X coordinate is not close to the step X coordinate.
plate = plate.edges("|Z").filter(lambda e: abs(e.Center().x - L_narrow) > 0.1).fillet(R_fillet)

# 2. Create the Vertical Web/Rib
# The web runs the full length of the part and is extruded downwards.
# It is centered relative to the narrow section's width (W_narrow).
web = (
    cq.Workplane("XY")
    .rect(L_total, T_web)
    .extrude(-H_web)
)

# Position the web
# The rectangle is created at (0,0), so we move it to the correct center position.
# X center: Half of total length
# Y center: Half of the narrow width
web = web.translate((L_total / 2, W_narrow / 2, 0))

# 3. Combine to form the final part
result = plate.union(web)