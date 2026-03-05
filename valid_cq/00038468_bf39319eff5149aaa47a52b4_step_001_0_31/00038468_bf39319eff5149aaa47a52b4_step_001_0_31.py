import cadquery as cq

# Parameters for the ellipsoid
# The image shows a vertically elongated shape, so radius_z is larger
radius_x = 12.0
radius_y = 12.0 # Implied by revolve
radius_z = 36.0

# Create the ellipsoid
# 1. Create a workplane on XZ
# 2. Draw an elliptical arc for the right half (270 degrees to 90 degrees)
# 3. Close the profile (creates straight lines along the vertical axis)
# 4. Revolve 360 degrees around the local Y axis (global Z axis)
result = (
    cq.Workplane("XZ")
    .ellipseArc(radius_x, radius_z, 270, 90)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)