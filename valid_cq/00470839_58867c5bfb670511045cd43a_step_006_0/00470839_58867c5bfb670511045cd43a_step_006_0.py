import cadquery as cq

# Parameters for the dimensions of the trapezoidal fin
height_right_edge = 90.0   # Vertical height of the straight right edge
height_left_peak = 110.0   # Height of the top-left corner
width_top = 40.0           # Horizontal width at the top
width_bottom = 12.0        # Horizontal width at the bottom
thickness = 3.0            # Thickness of the plate

# Define the vertices of the shape on the XZ plane (standing vertically)
# Coordinates are (X, Z) relative to the bottom-right corner at (0,0)
points = [
    (0, 0),                          # Bottom Right
    (0, height_right_edge),          # Top Right
    (-width_top, height_left_peak),  # Top Left
    (-width_bottom, 0)               # Bottom Left
]

# Create the 3D model
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .extrude(thickness)
)