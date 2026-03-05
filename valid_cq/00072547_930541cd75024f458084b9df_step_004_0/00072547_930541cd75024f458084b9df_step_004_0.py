import cadquery as cq

# Parametric dimensions
major_radius = 40.0  # Radius from the center of the ring to the center of the tube
minor_radius = 3.0   # Radius of the tube cross-section (thickness)

# Create the torus geometry
# 1. Initialize a Workplane on the XZ plane.
# 2. Move the drawing cursor away from the origin by the major_radius.
# 3. Draw the circular cross-section of the ring.
# 4. Revolve the cross-section 360 degrees around the Z-axis (0,0,1) to form the ring.
result = (
    cq.Workplane("XZ")
    .center(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)