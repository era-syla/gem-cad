import cadquery as cq
import math

# Parameters
num_teeth = 20
outer_radius = 30
inner_radius = 25
height = 45

# Build the gear-like profile using a polygon approximation with sine wave
points = []
num_points = num_teeth * 8  # points per tooth cycle

for i in range(num_points):
    angle = 2 * math.pi * i / num_points
    # Radius varies sinusoidally to create teeth
    r = inner_radius + (outer_radius - inner_radius) * 0.5 * (1 + math.sin(num_teeth * angle))
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    points.append((x, y))

# Close the polygon by repeating the first point
points.append(points[0])

# Create the profile and extrude
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(height)
)