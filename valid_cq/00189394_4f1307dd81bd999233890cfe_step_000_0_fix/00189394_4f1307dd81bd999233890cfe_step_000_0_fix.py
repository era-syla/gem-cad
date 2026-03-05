import cadquery as cq

# Create a list of points for the shape
points = [
    (0, 4), (1, 5), (3, 4), (4, 3), (5, 2), (5, -1), 
    (3, -2), (1, -3), (-1, -2), (-3, -1), (-4, 0), (-3, 2)
]

# Create the 2D profile on the XY plane
profile = cq.Workplane("XY").polyline(points).close()

# Extrude the profile to create the 3D shape
result = profile.extrude(1)