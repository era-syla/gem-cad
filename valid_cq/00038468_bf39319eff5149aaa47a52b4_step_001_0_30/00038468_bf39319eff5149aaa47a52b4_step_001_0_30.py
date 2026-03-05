import cadquery as cq

# Parameters for the ellipsoid shape
# Based on visual estimation, the shape is a prolate spheroid
# approximately 2.5 times taller than it is wide.
radius = 12.0       # Equatorial radius (along X/Y)
semi_height = 30.0  # Polar radius (half of total height along Z)

# Generate the geometry
# We create a profile on the XZ plane and revolve it around the Z axis.
result = (
    cq.Workplane("XZ")
    # Draw a semi-elliptical arc.
    # On the XZ plane: 
    #   0 degrees is +X
    #   90 degrees is +Z (Local Y)
    #   270 degrees is -Z
    # We draw from bottom (-Z) to top (+Z) sweeping through +X.
    .ellipseArc(x_radius=radius, y_radius=semi_height, angle1=270, angle2=90)
    # Close the profile with a straight line along the Z-axis to form a closed wire
    .close()
    # Revolve the closed profile 360 degrees around the vertical axis (Local Y / Global Z)
    .revolve()
)