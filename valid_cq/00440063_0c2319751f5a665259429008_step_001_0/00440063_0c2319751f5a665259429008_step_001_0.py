import cadquery as cq

# Parametric dimensions for the triangle vertices
# Coordinates approximate the scalene triangle shape visible in the image
v1 = (0, 0)        # Leftmost vertex (origin)
v2 = (80, 25)      # Top-right vertex
v3 = (65, -45)     # Bottom-right vertex
plate_thickness = 2.0

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .polyline([v1, v2, v3])
    .close()
    .extrude(plate_thickness)
)