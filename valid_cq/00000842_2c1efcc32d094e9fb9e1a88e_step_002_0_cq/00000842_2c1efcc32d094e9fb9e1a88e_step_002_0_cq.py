import cadquery as cq

# Parametric dimensions
side_length = 50.0  # Length of the triangle side
thickness = 2.0     # Thickness of the plate
fillet_radius = 1.0 # Radius for the corner fillets

# Create the triangle profile
# We'll create a polygon for an equilateral triangle.
# The height of an equilateral triangle is (sqrt(3)/2) * side_length
import math
height = (math.sqrt(3) / 2) * side_length

# Coordinates for an equilateral triangle centered roughly around the origin
# Top vertex
p1 = (0, 2 * height / 3)
# Bottom right vertex
p2 = (side_length / 2, -height / 3)
# Bottom left vertex
p3 = (-side_length / 2, -height / 3)

# Create the base shape
result = (
    cq.Workplane("XY")
    .polyline([p1, p2, p3])
    .close()
    .extrude(thickness)
)

# Apply fillets to the vertical edges
result = result.edges("|Z").fillet(fillet_radius)