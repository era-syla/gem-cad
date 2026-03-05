import cadquery as cq

# Geometric parameters
major_radius = 40.0  # The radius of the ring (distance from center to tube center)
minor_radius = 5.0   # The radius of the tube cross-section

# Create the torus
# 1. Select the XZ plane for the cross-section sketch.
#    (Note: On the XZ plane, the local Y axis aligns with the global Z axis)
# 2. Move the work center to the major radius distance along the X axis.
# 3. Draw the circular cross-section.
# 4. Revolve the profile 360 degrees.
#    (Default axis for revolve on XZ plane is local Y, which is global Z)
result = (
    cq.Workplane("XZ")
    .moveTo(major_radius, 0)
    .circle(minor_radius)
    .revolve()
)