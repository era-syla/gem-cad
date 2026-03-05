import cadquery as cq
from cadquery import Vector

# Define the 3D path points
points = [
    Vector(0, 0, 0),
    Vector(2, 1.5, 0),
    Vector(5, 0.5, 0),
    Vector(8, -1, 0),
    Vector(12, -0.5, 0),
    Vector(16, 2, 0),
    Vector(20, 0.5, 0),
    Vector(24, -1.5, 0),
    Vector(28, 0, 0),
    Vector(30, 0, 0)
]

# Create a spline edge through the points
path_edge = cq.Edge.makeSpline(points)

# Sweep a circular profile along the spline to make the tube
result = cq.Workplane("XY") \
    .circle(0.5) \
    .sweep(path_edge)