import cadquery as cq

# Define parametric dimensions
side_length = 50.0  # Length of the triangle side (approximate)
thickness = 2.0     # Thickness of the plate

# Create a triangle
# Using a polygon to define the 3 vertices of the triangle centered at origin
# An equilateral triangle for symmetry
import math
height = side_length * math.sqrt(3) / 2
p1 = (0, height * 2/3)
p2 = (-side_length / 2, -height / 3)
p3 = (side_length / 2, -height / 3)

# Create the sketch and extrude
result = (
    cq.Workplane("XY")
    .polyline([p1, p2, p3])
    .close()
    .extrude(thickness)
)