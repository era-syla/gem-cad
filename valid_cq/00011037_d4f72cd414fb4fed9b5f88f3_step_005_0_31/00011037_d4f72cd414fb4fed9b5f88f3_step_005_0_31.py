import cadquery as cq

# Parametric dimensions
length = 100.0
height = 65.0
thickness = 25.0
chamfer_x = 35.0  # Horizontal distance from the left edge to the start of the top flat
chamfer_y = 25.0  # Vertical distance from the bottom edge to the start of the angled cut

# Define the points for the 2D profile
profile_points = [
    (0, 0),
    (length, 0),
    (length, height),
    (chamfer_x, height),
    (0, chamfer_y)
]

# Create the solid by extruding the closed profile
result = (
    cq.Workplane("front")
    .polyline(profile_points)
    .close()
    .extrude(thickness)
)