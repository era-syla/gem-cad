import cadquery as cq
import math

# Define a list of cross‐section profiles (2D point lists) at various X stations
profiles = [
    (0.0,  [(-10, 0), (-5,  4), (0, 5),  (5,  4),  (10, 0),  (5, -4),  (0, -5),  (-5, -4)]),
    (15.0, [(-8,  0), (-4,  3), (0, 3.5),(4,  3),  (8,  0),  (4, -3),  (0, -3.5),(-4, -3)]),
    (30.0, [(-6,  0), (-3,  2), (0, 2.5),(3,  2),  (6,  0),  (3, -2),  (0, -2.5),(-3, -2)]),
    (45.0, [(-4,  0), (-2,  1), (0, 1.5),(2,  1),  (4,  0),  (2, -1),  (0, -1.5),(-2, -1)]),
    (60.0, [(-2,  0), (-1,  0.5),(0, 0.75),(1,  0.5),(2,  0),  (1, -0.5),(0, -0.75),(-1, -0.5)])
]

# Start on the YZ plane so that offset moves along the X axis
wp = cq.Workplane("YZ")
for station_x, pts in profiles:
    # For each station, move along X and draw the 2D profile in the YZ plane
    wp = wp.workplane(offset=station_x).polyline(pts).close()

# Loft through all the profiles to get a smooth 3D solid
result = wp.loft() 