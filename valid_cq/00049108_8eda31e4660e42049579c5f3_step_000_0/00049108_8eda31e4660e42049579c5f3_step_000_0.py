import cadquery as cq

# Parametric dimensions for the cylinder
cyl_radius = 25.0
cyl_height = 70.0
shoulder_height = 20.0
neck_radius = 8.0
neck_straight_height = 3.0
knob_radius = 10.0
knob_height = 7.0
fillet_radius = 8.0

# Calculate vertical positions
z_shoulder_start = cyl_height
z_neck_start = z_shoulder_start + shoulder_height
z_knob_start = z_neck_start + neck_straight_height
z_top = z_knob_start + knob_height

# Create the profile on the XZ plane to be revolved
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(cyl_radius, 0)                 # Bottom base
    .lineTo(cyl_radius, z_shoulder_start)  # Cylinder body
    
    # Create the shoulder using a spline for a smooth, organic transition
    # Tangents are set to vertical (0, 1) at both ends to ensure smooth blending
    .spline(
        [(neck_radius, z_neck_start)],
        tangents=[(0, 1), (0, 1)],
        includeCurrent=True
    )
    
    # Straight vertical section of the neck
    .lineTo(neck_radius, z_knob_start)
    
    # Create the valve/knob feature at the top
    # Use a 3-point arc to create a bulbous shape that terminates at the center axis
    .threePointArc(
        (knob_radius, z_knob_start + knob_height * 0.4), # Mid-point (bulge)
        (0, z_top)                                       # End-point (top center)
    )
    .close()
)

# Revolve the profile 360 degrees around the Z-axis to create the solid
result = profile.revolve()

# Apply a fillet to the bottom edge for the rounded base look
result = result.faces("<Z").edges().fillet(fillet_radius)