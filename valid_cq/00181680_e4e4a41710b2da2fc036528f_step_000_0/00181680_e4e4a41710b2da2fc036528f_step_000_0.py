import cadquery as cq

# Parameters for the model
thickness = 5.0  # Thickness of the extruded shape
scale_factor = 1.0

# Define control points for the spline to recreate the organic 'splat' shape.
# Coordinates are defined as (x, y) tuples moving clockwise around the shape.
# The points alternate between lobe tips (outer) and valleys (inner).
control_points = [
    (20, 95),    # Top Lobe Tip
    (32, 60),    # Valley
    (65, 80),    # Top-Right Lobe Tip
    (50, 40),    # Valley
    (80, 15),    # Right Lobe Tip
    (45, -15),   # Valley
    (50, -50),   # Bottom-Right Lobe Tip
    (10, -40),   # Valley
    (-15, -95),  # Bottom Lobe Tip
    (-35, -40),  # Valley (Deep)
    (-70, -65),  # Bottom-Left Lobe Tip
    (-50, -10),  # Valley
    (-75, 20),   # Left Lobe Tip
    (-40, 45),   # Valley
    (-30, 75),   # Top-Left Lobe Tip
    (0, 60)      # Valley
]

# Apply scaling if necessary
points = [(x * scale_factor, y * scale_factor) for x, y in control_points]

# Generate the 3D geometry
result = (
    cq.Workplane("XY")
    .spline(points)
    .close()
    .extrude(thickness)
)