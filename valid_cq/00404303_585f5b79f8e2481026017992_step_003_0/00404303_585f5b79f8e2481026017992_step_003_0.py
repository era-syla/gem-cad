import cadquery as cq

# Geometric parameters
major_radius = 50.0  # Radius from the center of the ring to the center of the tube
minor_radius = 4.0   # Radius of the tube cross-section (thickness)

# Create the torus using a revolve operation
# 1. Select the XZ plane to draw the cross-section
# 2. Offset the drawing center by the major_radius
# 3. Draw the circular cross-section
# 4. Revolve the cross-section 360 degrees around the Z-axis
result = (
    cq.Workplane("XZ")
    .center(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)