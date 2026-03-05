import cadquery as cq
import math

# Dimensions for the ellipsoid
height = 60.0       # Total height along the Z axis
diameter = 24.0     # Maximum diameter in the XY plane

# Generate points for a semi-elliptical profile in the XZ plane
# We define the right half of the ellipse (x >= 0)
points = []
num_points = 40

for i in range(num_points + 1):
    # Parameter t varies from -pi/2 (bottom pole) to pi/2 (top pole)
    t = -math.pi / 2 + (math.pi * i / num_points)
    
    # Parametric equations for an ellipse:
    # x = (width/2) * cos(t)
    # z = (height/2) * sin(t)
    x = (diameter / 2.0) * math.cos(t)
    z = (height / 2.0) * math.sin(t)
    
    # Force x to 0 at the poles to ensure a closed clean solid on the axis
    if i == 0 or i == num_points:
        x = 0.0
        
    points.append((x, z))

# Separate the start point to initialize the path
start_p = points[0]
path_points = points[1:]

# Create the ellipsoid by revolving the spline profile
result = (
    cq.Workplane("XZ")
    .moveTo(start_p[0], start_p[1])
    .spline(path_points)  # Create a smooth curve through the points
    .close()              # Close the wire along the Z-axis
    .revolve(360, (0, 0, 0), (0, 1, 0))  # Revolve around the Z-axis (local Y of XZ plane)
)