import cadquery as cq

# Parametric dimensions
thickness = 1.0

# Approximate coordinates for the simplified Texas map profile
pts = [
    (-1.0, 5.0),   # Panhandle Top-Left
    (1.0, 5.0),    # Panhandle Top-Right
    (1.0, 2.5),    # Panhandle Bottom-Right
    (2.5, 2.8),    # Red River jagged points
    (3.0, 2.0),
    (4.5, 2.2),
    (5.0, 1.0),
    (4.8, -0.5),   # Sabine River
    (3.5, -2.0),   # Gulf Coast inward curve
    (4.0, -3.5),   # Gulf Coast outward curve
    (2.0, -5.0),
    (0.5, -6.0),   # Southern Tip (Brownsville)
    (-0.5, -5.0),  # Rio Grande jagged points up
    (-0.2, -3.5),
    (-2.0, -2.0),  # Big Bend area
    (-1.0, -1.0),
    (-3.5, 0.0),
    (-4.0, 1.5),   # El Paso area bottom
    (-4.0, 2.5),   # El Paso area top (NM border start)
    (-1.0, 2.5)    # NM border corner
]

# Create the 3D model by drawing the polyline and extruding it
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)