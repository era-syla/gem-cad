import cadquery as cq

# Parametric dimensions for the model
height = 60.0        # Total height of the number '3'
width = 35.0         # Total width (spine + arms)
depth = 15.0         # Extrusion depth (thickness of the 3D object)
bar_thickness = 12.0 # Thickness of the horizontal arms and vertical spine

# Derived calculations for geometry points
h_mid = height / 2.0
t_half = bar_thickness / 2.0

# Define points for the '3' profile on the XZ plane to orient it upright
# Coordinates assume origin (0,0) is at the bottom-left outer corner
# The shape traces the outer boundary and the inner voids
points = [
    (0, height),                                      # 1. Top-left outer tip
    (width, height),                                  # 2. Top-right outer corner
    (width, 0),                                       # 3. Bottom-right outer corner
    (0, 0),                                           # 4. Bottom-left outer tip
    (0, bar_thickness),                               # 5. Bottom arm tip (up)
    (width - bar_thickness, bar_thickness),           # 6. Bottom arm inner corner
    (width - bar_thickness, h_mid - t_half),          # 7. Middle arm lower inner corner
    (0, h_mid - t_half),                              # 8. Middle arm lower tip
    (0, h_mid + t_half),                              # 9. Middle arm upper tip
    (width - bar_thickness, h_mid + t_half),          # 10. Middle arm upper inner corner
    (width - bar_thickness, height - bar_thickness),  # 11. Top arm inner corner
    (0, height - bar_thickness),                      # 12. Top arm tip (down)
    (0, height)                                       # 13. Close loop back to start
]

# Generate the solid geometry
result = (
    cq.Workplane("XZ")  # Draw on Front plane
    .polyline(points)
    .close()
    .extrude(depth)
)