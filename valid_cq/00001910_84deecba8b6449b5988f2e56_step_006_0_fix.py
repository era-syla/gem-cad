import cadquery as cq

# Create a decorative finial/newel post cap shape
# Components: base flange, lower sphere, upper sphere, top disk with hole

# Use revolve to create the profile
# Define 2D profile points for revolve around Y axis

import cadquery as cq

def make_profile():
    # Profile defined as a series of points for revolve
    # The shape has:
    # - flat base flange at bottom
    # - small neck/pedestal
    # - large lower bulb (sphere-like)
    # - small waist
    # - upper bulb (sphere-like, slightly smaller)
    # - top disk/flange with center hole
    
    # We'll build this by revolving a 2D profile
    # Points go from bottom to top, defining the outer edge
    
    pts = [
        # Base flange outer edge
        (0, 0),
        (30, 0),
        (30, 3),
        (20, 5),
        (15, 8),
        # Lower bulge
        (28, 20),
        (30, 35),
        (28, 50),
        # Waist between bulges
        (18, 58),
        # Upper bulge
        (25, 65),
        (27, 75),
        (25, 85),
        # Neck to top disk
        (15, 90),
        (15, 93),
        (28, 95),
        (28, 100),
        # Inner top disk edge (hole)
        (7, 100),
        (7, 95),
        # Inner profile going back down
        (12, 93),
        (12, 90),
        # Close back through center
        (5, 85),
        (5, 65),
        (5, 58),
        (5, 50),
        (5, 20),
        (5, 8),
        (5, 5),
        (5, 3),
        (5, 0),
        (0, 0),
    ]
    return pts

# Build using revolve with a spline profile
# Use wire/edge approach

result = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (30, 0),
        (30, 3),
        (20, 6),
        (14, 10),
    ])
    .spline([
        (14, 10),
        (30, 25),
        (32, 40),
        (28, 55),
        (18, 62),
    ])
    .spline([
        (18, 62),
        (26, 68),
        (28, 78),
        (24, 88),
        (14, 93),
    ])
    .polyline([
        (14, 93),
        (14, 95),
        (28, 97),
        (28, 103),
        (6, 103),
        (6, 97),
        (10, 95),
        (10, 93),
    ])
    .spline([
        (10, 93),
        (6, 85),
        (4, 78),
        (5, 68),
        (10, 62),
    ])
    .spline([
        (10, 62),
        (4, 55),
        (2, 40),
        (5, 25),
        (10, 10),
    ])
    .polyline([
        (10, 10),
        (5, 6),
        (3, 3),
        (3, 0),
        (0, 0),
    ])
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)