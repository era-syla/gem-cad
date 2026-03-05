import cadquery as cq

# Parametric dimensions
major_radius = 50.0  # Radius from the center of the ring to the center of the tube
minor_radius = 5.0   # Radius of the tube itself (thickness)

# Generate the torus geometry
# 1. Create a workplane on the XZ plane (side view)
# 2. Move to the major radius offset on the X axis
# 3. Create the circular cross-section of the tube
# 4. Revolve the cross-section 360 degrees around the Z axis
#    Note: On the XZ plane, the local Y axis corresponds to the global Z axis.
#    We revolve around the origin (0,0) to (0,1) in local coordinates.
result = (
    cq.Workplane("XZ")
    .moveTo(major_radius, 0)
    .circle(minor_radius)
    .revolve(360, (0, 0, 0), (0, 1, 0))
)