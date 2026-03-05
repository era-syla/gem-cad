import cadquery as cq

# Parametric dimensions for the torus
major_radius = 50.0  # The radius from the center of the ring to the center of the tube
tube_radius = 5.0    # The radius of the tube cross-section

# Create the 3D model
# 1. Select the XZ plane to draw the cross-section vertically
# 2. Move the drawing cursor away from the origin by the major_radius
# 3. Draw the circular cross-section
# 4. Revolve the cross-section 360 degrees around the Z-axis (0,0,1)
result = (
    cq.Workplane("XZ")
    .moveTo(major_radius, 0)
    .circle(tube_radius)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)