import cadquery as cq

# Parametric dimensions
length = 150.0
width = 20.0
height = 20.0

# Construction of a Quarter-Round Rail
# Method: Intersection of a Box and a Cylinder to ensure perfect curvature and tangency.
# Orientation: Length along X-axis.

# 1. Create the bounding box
# Centered at origin, so it extends from -L/2 to L/2 in X, -W/2 to W/2 in Y, -H/2 to H/2 in Z
box = cq.Workplane("XY").box(length, width, height)

# 2. Create a cylinder to intersect with
# We align the cylinder's axis with the "Top-Back" edge of the box.
# Assuming "Back" is -Y and "Top" is +Z: Edge is at y = -width/2, z = height/2.
# The cylinder radius equals the width/height to create a full quadrant profile.
cylinder = (
    cq.Workplane("YZ")
    .circle(width)  # Radius matches the cross-section size
    .extrude(length)
    # Move cylinder to align with the box:
    # 1. Center in X (extrude starts at 0, box starts at -L/2)
    # 2. Align center to the top-back edge of the box
    .translate((-length / 2.0, -width / 2.0, height / 2.0))
)

# 3. Intersect the two shapes
# This keeps the material common to both, resulting in a convex quarter-round profile
# with a flat top and flat back.
result = box.intersect(cylinder)