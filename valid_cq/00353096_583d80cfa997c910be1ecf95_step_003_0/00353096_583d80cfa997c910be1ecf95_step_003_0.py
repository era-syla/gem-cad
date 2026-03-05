import cadquery as cq

# Parametric dimensions
major_radius = 40.0  # Radius from the center of the ring to the center of the cross-section
minor_radius = 4.0   # Radius of the tube cross-section (thickness)

# Create the torus geometry
# 1. Use the XZ plane to sketch the cross-section vertically
# 2. Move the sketch position away from the center by the major_radius
# 3. Draw the circular cross-section
# 4. Revolve the circle 360 degrees around the Z-axis (which is the local Y-axis of the XZ plane)
result = (
    cq.Workplane("XZ")
    .moveTo(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 1, 0))
)