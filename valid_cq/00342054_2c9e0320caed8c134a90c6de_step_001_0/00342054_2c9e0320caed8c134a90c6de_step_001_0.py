import cadquery as cq
import math

# Parameters defining the geometry
num_points = 5
outer_radius = 50.0
inner_radius = 26.0
thickness = 15.0
hole_diameter = 25.0
tip_fillet = 6.0
valley_fillet = 8.0

# Calculate the vertices for the star profile
points = []
for i in range(2 * num_points):
    # Calculate angle in radians
    # Offset by 90 degrees (pi/2) so the first point points upwards in Y
    angle = (math.pi / 2) + (i * math.pi / num_points)
    
    # Alternate between outer and inner radius
    r = outer_radius if i % 2 == 0 else inner_radius
    
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    points.append((x, y))

# Create the base solid by extruding the profile
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)

# Calculate a radius threshold to distinguish tips from valleys
# Edges further than this are tips, closer are valleys
threshold_radius = (outer_radius + inner_radius) / 2

# Apply fillets to the outer tips
# Select vertical edges and filter based on radial distance
edges_tips = [
    e for e in result.edges("|Z").vals() 
    if (e.Center().x**2 + e.Center().y**2)**0.5 > threshold_radius
]
result = result.newObject(edges_tips).fillet(tip_fillet)

# Apply fillets to the inner valleys
# Re-select vertical edges as topology has changed after the first fillet
edges_valleys = [
    e for e in result.edges("|Z").vals() 
    if (e.Center().x**2 + e.Center().y**2)**0.5 < threshold_radius
]
result = result.newObject(edges_valleys).fillet(valley_fillet)

# Cut the central through-hole
result = result.faces(">Z").workplane().hole(hole_diameter)