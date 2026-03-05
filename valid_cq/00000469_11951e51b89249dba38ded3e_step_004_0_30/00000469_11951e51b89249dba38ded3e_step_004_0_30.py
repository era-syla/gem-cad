import cadquery as cq

# Parametric dimensions for the torus (O-ring)
major_radius = 40.0  # Distance from the center of the ring to the center of the tube
minor_radius = 4.0   # Radius of the tube's cross-section

# Generate the torus geometry
# 1. Initialize a workplane on the XZ plane to draw the cross-section vertical to the floor
# 2. Offset the center by the major_radius to define the ring size
# 3. Draw the circular cross-section
# 4. Revolve the cross-section 360 degrees around the Z-axis to create the ring
result = (
    cq.Workplane("XZ")
    .center(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 0, 1))
)