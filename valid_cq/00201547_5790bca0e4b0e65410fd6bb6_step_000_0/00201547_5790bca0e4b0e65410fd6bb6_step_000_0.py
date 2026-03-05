import cadquery as cq

# Geometric parameters based on visual estimation
length = 80.0
width = 45.0
thickness = 6.0
corner_radius = 8.0

# Create the rounded rectangular plate
# 1. Create a base box centered on the XY plane
# 2. Select edges parallel to the Z axis (vertical corners)
# 3. Apply fillet to round the corners
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z")
    .fillet(corner_radius)
)