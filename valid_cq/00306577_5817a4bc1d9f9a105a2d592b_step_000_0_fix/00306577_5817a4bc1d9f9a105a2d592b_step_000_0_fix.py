import cadquery as cq

# Define the profile for the pawn body and base in the XZ-plane
profile = [
    (12, 0),
    (12, 3),
    (10, 5),
    (8, 14),
    (7, 30),
    (12, 30),
    (12, 32),
    (0, 32),
]

# Revolve the profile around the Y-axis to create the lower body
lower = cq.Workplane("XZ").polyline(profile).close().revolve(360, (0, 0, 0), (0, 1, 0))

# Create the spherical head and position it on top
sphere = cq.Workplane("XY").sphere(8).translate((0, 0, 40))

# Combine the lower body and the head into the final result
result = lower.union(sphere)