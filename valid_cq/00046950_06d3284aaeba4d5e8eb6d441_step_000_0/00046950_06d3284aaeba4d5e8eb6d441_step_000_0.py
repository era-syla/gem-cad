import cadquery as cq

# Model parameters
width = 40.0
height_back = 30.0
height_front = 5.0
length_top_flat = 30.0
length_slope_run = 30.0
length_bottom_flat = 40.0

# Calculate x-coordinates for profile points
x1 = length_top_flat
x2 = length_top_flat + length_slope_run
x3 = length_top_flat + length_slope_run + length_bottom_flat

# Define the points for the side profile (XZ plane)
# Starting from origin (0,0) at bottom-back corner
points = [
    (0, 0),
    (0, height_back),
    (x1, height_back),
    (x2, height_front),
    (x3, height_front),
    (x3, 0)
]

# Create the 3D model
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .extrude(width)
)