import cadquery as cq
import math

# Parameters
num_teeth = 12
radius_outer = 10
radius_inner = 9
height = 30

# Build the 2D gear profile
points = []
for i in range(2 * num_teeth):
    angle = i * math.pi / num_teeth
    r = radius_outer if (i % 2 == 0) else radius_inner
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    points.append((x, y))

# Create the 3D gear by extruding the profile
result = (
    cq.Workplane("XY")
      .polyline(points)
      .close()
      .extrude(height)
)