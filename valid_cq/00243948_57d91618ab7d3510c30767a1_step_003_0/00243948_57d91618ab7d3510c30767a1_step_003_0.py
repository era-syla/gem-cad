import cadquery as cq

# Define parametric dimensions for the torus
major_radius = 50.0  # Distance from the center of the torus to the center of the tube
minor_radius = 4.0   # Radius of the tube cross-section

# Create the torus geometry
# We define the cross-section on the XZ plane, offset by the major_radius,
# and revolve it around the Z-axis (which is the vertical axis relative to the XY plane).
result = (
    cq.Workplane("XZ")
    .moveTo(major_radius, 0)
    .circle(minor_radius)
    .revolve()  # Defaults to 360 degrees around the workplane's Y-axis (Global Z)
)