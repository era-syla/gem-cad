import cadquery as cq

# Parametric dimensions for the hexagonal/octagonal plate
overall_length = 100.0      # Total length in X
overall_width = 60.0        # Total width in Y
thickness = 5.0             # Plate thickness
top_flat_length = 50.0      # Length of the top and bottom horizontal segments
side_flat_height = 15.0     # Height of the vertical segments at the ends

# Calculate half-dimensions for coordinate definitions
x_mid = top_flat_length / 2.0
x_end = overall_length / 2.0
y_mid = side_flat_height / 2.0
y_end = overall_width / 2.0

# Define vertices for the polygon profile (Counter-Clockwise order)
points = [
    (x_mid, y_end),     # Top edge, right point
    (-x_mid, y_end),    # Top edge, left point
    (-x_end, y_mid),    # Left edge, top point
    (-x_end, -y_mid),   # Left edge, bottom point
    (-x_mid, -y_end),   # Bottom edge, left point
    (x_mid, -y_end),    # Bottom edge, right point
    (x_end, -y_mid),    # Right edge, bottom point
    (x_end, y_mid)      # Right edge, top point
]

# Create the 3D solid
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)