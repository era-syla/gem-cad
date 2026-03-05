import cadquery as cq

# Parametric dimensions
major_radius = 40.0  # Radius from the center of the ring to the center of the tube
minor_radius = 4.0   # Radius of the tube's cross-section

# Create the torus geometry
# 1. Initialize a workplane on the XZ plane
# 2. Offset the center to the major_radius
# 3. Draw the circular cross-section
# 4. Revolve the cross-section 360 degrees around the Z-axis (defined by points (0,0,0) and (0,0,1))
result = (
    cq.Workplane("XZ")
    .center(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)