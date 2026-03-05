import cadquery as cq

# Parametric dimensions based on the visual estimation of the image
inner_radius = 45.0      # Radius of the inner curve
profile_width = 15.0     # Radial width of the rectangular cross-section
profile_thickness = 15.0 # Lateral thickness of the cross-section
arc_angle = 90.0         # Angle of the arc (quarter circle)

# Calculate the center offset for the profile
# The profile center is positioned at the inner radius + half the width
center_offset = inner_radius + (profile_width / 2.0)

# Generate the 3D model
# We start on the XY plane, draw the profile offset along X, 
# and revolve it around the Y-axis to create a vertical arch.
# Revolving around (0,0,0)->(0,-1,0) sweeps the X-axis towards the Z-axis (Right-Hand Rule)
result = (
    cq.Workplane("XY")
    .moveTo(center_offset, 0)
    .rect(profile_width, profile_thickness)
    .revolve(arc_angle, (0, 0, 0), (0, -1, 0))
)