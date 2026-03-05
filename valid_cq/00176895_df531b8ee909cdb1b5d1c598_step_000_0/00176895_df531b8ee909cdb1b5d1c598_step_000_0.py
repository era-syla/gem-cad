import cadquery as cq

# Parameters for the elongated hexagon (coffin shape)
total_length = 100.0    # Total length from point to point along X axis
total_width = 50.0      # Total width along Y axis
thickness = 5.0         # Thickness of the extrusion
straight_length = 50.0  # Length of the parallel top and bottom edges

# Calculate vertex coordinates based on symmetry
x_tip = total_length / 2.0
x_straight = straight_length / 2.0
y_outer = total_width / 2.0

# Define the points of the polygon in counter-clockwise order
points = [
    (x_tip, 0),               # Right tip
    (x_straight, y_outer),    # Top right
    (-x_straight, y_outer),   # Top left
    (-x_tip, 0),              # Left tip
    (-x_straight, -y_outer),  # Bottom left
    (x_straight, -y_outer)    # Bottom right
]

# Create the 3D object
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)