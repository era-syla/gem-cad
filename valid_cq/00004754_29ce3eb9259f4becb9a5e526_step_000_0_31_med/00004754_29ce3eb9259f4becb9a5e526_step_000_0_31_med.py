import cadquery as cq
import math

# Parametric dimensions
radius = 10.0
height = 60.0
twist_angle = 90.0
cut_dist = 5.0  # Distance from the center to the flat edge

# Calculate intersection points for the D-profile
y_intersect = math.sqrt(radius**2 - cut_dist**2)

# Create the twisted D-shaft
result = (
    cq.Workplane("XY")
    .moveTo(-cut_dist, y_intersect)
    .lineTo(-cut_dist, -y_intersect)
    .threePointArc((radius, 0), (-cut_dist, y_intersect))
    .close()
    .twistExtrude(height, twist_angle)
)