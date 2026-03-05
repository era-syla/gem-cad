import cadquery as cq
import math

# --- Parameters ---
outer_radius = 50.0   # Radius of the outer points
inner_radius = 25.0   # Radius of the inner points (indentation)
thickness = 5.0       # Extrusion thickness
num_points = 5        # Number of star points

# --- Geometry Calculation ---
points = []
angle_step = math.pi / num_points  # Angle between each vertex (outer/inner)
start_angle = math.pi / 2          # Start at 90 degrees (top vertical)

# Calculate the vertices of the star
for i in range(2 * num_points):
    # Alternate between outer and inner radius
    r = outer_radius if i % 2 == 0 else inner_radius
    theta = start_angle + i * angle_step
    
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    points.append((x, y))

# --- Model Construction ---
# Initialize workplane
wp = cq.Workplane("XY")

# Move to the first point without drawing
wp = wp.moveTo(points[0][0], points[0][1])

# Draw lines to the remaining points using absolute coordinates
for point in points[1:]:
    wp = wp.lineTo(point[0], point[1])

# Close the wire and extrude to create the solid
result = wp.close().extrude(thickness)