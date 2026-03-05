import cadquery as cq

# Parametric dimensions
long_leg_length = 80.0   # Length of the longer leg
short_leg_length = 50.0  # Length of the shorter leg
leg_width = 15.0         # Width of the L-profile
thickness = 10.0         # Thickness (extrusion depth)

# Create the L-bracket geometry
# We sketch the profile on the XY plane starting from the origin (outer corner)
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(long_leg_length, 0)                # Outer edge of long leg
    .lineTo(long_leg_length, leg_width)        # End of long leg
    .lineTo(leg_width, leg_width)              # Inner corner
    .lineTo(leg_width, short_leg_length)       # Inner edge of short leg
    .lineTo(0, short_leg_length)               # End of short leg
    .close()
    .extrude(thickness)
)