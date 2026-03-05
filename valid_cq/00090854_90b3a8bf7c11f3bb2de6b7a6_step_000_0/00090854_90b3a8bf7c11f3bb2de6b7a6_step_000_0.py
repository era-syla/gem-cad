import cadquery as cq
import math

# Parameters for the star geometry
num_points = 5
outer_radius = 10.0
inner_radius = 4.0
thickness = 2.0

# Calculate the vertices of the star
vertices = []
for i in range(2 * num_points):
    # Angle calculation: 
    # Distribute points evenly around circle (360 degrees)
    # Start at 90 degrees to have a point pointing straight up
    angle_deg = 90 - (i * 360.0 / (2 * num_points))
    angle_rad = math.radians(angle_deg)
    
    # Toggle between outer and inner radius
    r = outer_radius if i % 2 == 0 else inner_radius
    
    # Polar to Cartesian coordinates
    x = r * math.cos(angle_rad)
    y = r * math.sin(angle_rad)
    vertices.append((x, y))

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .polyline(vertices)
    .close()
    .extrude(thickness)
)