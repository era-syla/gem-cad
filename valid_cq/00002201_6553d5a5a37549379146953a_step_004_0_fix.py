import cadquery as cq
import math

# Parameters
num_teeth = 16
outer_radius = 20
inner_radius = 16
height = 35

# Build the gear profile as a 2D closed wire by creating points around the circle
# Using sinusoidal variation to create the gear-like profile with rounded teeth
num_points = num_teeth * 20  # points per tooth * num_teeth

points = []
for i in range(num_points):
    angle = 2 * math.pi * i / num_points
    # Sinusoidal radius variation for smooth gear teeth
    r = inner_radius + (outer_radius - inner_radius) * 0.5 * (1 + math.sin(num_teeth * angle))
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    points.append((x, y))

# Close the polygon
points.append(points[0])

# Create the gear profile by extruding the 2D shape
result = (
    cq.Workplane("XY")
    .spline(points)
    .close()
    .extrude(height)
)