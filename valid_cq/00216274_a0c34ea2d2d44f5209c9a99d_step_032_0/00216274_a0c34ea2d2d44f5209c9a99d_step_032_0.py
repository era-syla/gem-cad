import cadquery as cq
import math

# Geometric parameters estimated from the image
length = 100.0      # Total vertical length
width = 6.0         # Width of the wider face
thickness = 1.5     # Thickness of the narrower face
cut_angle = 30.0    # Angle of the top slope in degrees

# Calculate the vertical height difference for the angled cut
# tan(angle) = height_diff / width
height_diff = width * math.tan(math.radians(cut_angle))

# Define the points for the 2D profile on the XZ plane.
# This creates a rectangular strip with an angled top edge.
# The profile is centered horizontally on the X-axis.
points = [
    (-width / 2, 0),                  # Bottom-left
    (width / 2, 0),                   # Bottom-right
    (width / 2, length - height_diff),# Top-right (lower point of the slope)
    (-width / 2, length)              # Top-left (higher point of the slope)
]

# Create the 3D solid
# 1. Initialize workplane on Front (XZ)
# 2. Draw the trapezoidal profile
# 3. Extrude to give thickness (Y direction)
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .extrude(thickness)
)