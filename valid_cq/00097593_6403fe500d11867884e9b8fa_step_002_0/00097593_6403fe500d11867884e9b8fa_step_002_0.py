import cadquery as cq

# Parametric dimensions based on visual estimation of the provided image
radius = 120.0      # Radius of the arc path (distance to center of profile)
width = 15.0        # Thickness of the profile (radial direction)
height = 25.0       # Height of the profile (vertical direction)
arc_angle = 60.0    # Angle of the arc segment in degrees

# Generate the 3D model
# 1. Select the XZ plane to draw the cross-section profile.
# 2. Move the drawing center to the specified radius along the X-axis.
# 3. Sketch a rectangular profile.
# 4. Revolve the profile around the Z-axis to create the curved solid.
result = (
    cq.Workplane("XZ")
    .center(radius, 0)
    .rect(width, height)
    .revolve(arc_angle, (0, 0, 0), (0, 0, 1))
)

# Center the geometry by rotating it backwards by half the arc angle
# This makes the part symmetric relative to the X-axis
result = result.rotate((0, 0, 0), (0, 0, 1), -arc_angle / 2)