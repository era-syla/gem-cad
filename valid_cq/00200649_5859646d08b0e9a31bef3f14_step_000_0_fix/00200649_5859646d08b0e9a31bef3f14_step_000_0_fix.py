import cadquery as cq

# Define a path for the sweep operation
path = cq.Workplane("XY").spline([(0, 0), (1, 1), (2, 0), (3, -1), (4, 0)])

# Define the cross-section profile
profile = cq.Workplane("XY").circle(0.5)

# Sweep the profile along the path
result = profile.sweep(path)