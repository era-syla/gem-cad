import cadquery as cq

# Parametric dimensions for the torus
major_radius = 20.0  # Radius from the center of the ring to the center of the tube
minor_radius = 2.0   # Radius of the tube cross-section (thickness)

# Create the torus geometry
# 1. Select the XZ plane to draw the cross-section profile
# 2. Offset the drawing center by the major radius
# 3. Draw the circular profile
# 4. Revolve the profile 360 degrees around the global Z-axis
result = (
    cq.Workplane("XZ")
    .center(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)