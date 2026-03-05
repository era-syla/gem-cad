import cadquery as cq

# Parametric dimensions
major_radius = 50.0  # Distance from the center of the ring to the center of the tube
minor_radius = 4.0   # Radius of the tube cross-section (thickness of the ring)

# Generate the torus geometry
# 1. Create a Workplane on the XZ plane.
# 2. Move the center of the sketch to the major_radius along the X axis.
# 3. Draw the cross-sectional circle with minor_radius.
# 4. Revolve the cross-section 360 degrees around the Z-axis (which is the local Y-axis of the XZ plane).
result = (
    cq.Workplane("XZ")
    .moveTo(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 1, 0))
)