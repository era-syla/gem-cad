import cadquery as cq

# Parametric dimensions based on the image geometry
length = 100.0       # Horizontal length
height_left = 30.0   # Height of the shorter vertical edge
height_right = 60.0  # Height of the taller vertical edge
thickness = 15.0     # Extrusion depth

# Generate the trapezoidal prism
# Sketch on the 'front' plane (XZ) to orient the heights vertically
result = (
    cq.Workplane("front")
    .polyline([
        (0, 0),                  # Bottom-left corner
        (length, 0),             # Bottom-right corner
        (length, height_right),  # Top-right corner
        (0, height_left)         # Top-left corner
    ])
    .close()
    .extrude(thickness)
)