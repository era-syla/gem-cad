import cadquery as cq
import math

# Parameters
R = 10.0        # Base radius
A = 2.0         # Amplitude of lobes
N = 12          # Number of lobes
H = 30.0        # Height of the cylinder
steps = 360     # Resolution of the profile

# Generate the 2D profile points
points = []
for i in range(steps):
    theta = 2 * math.pi * i / steps
    r = R + A * math.cos(N * theta)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    points.append((x, y))

# Build the 3D model
result = (
    cq.Workplane("XY")
      .polyline(points)
      .close()
      .extrude(H)
)