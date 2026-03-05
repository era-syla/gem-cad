import cadquery as cq

# Parametric dimensions for the horn/pseudosphere shape
length = 150.0
base_radius = 40.0

# Define control points for the spline to create a concave, exponential-like taper.
# The profile is defined in the XY plane and will be revolved around the X-axis.
# We start from the wide end and taper down to a sharp point.
profile_points = [
    (20.0, 18.0),   # Initial rapid flare down from the base
    (50.0, 7.0),    # Mid-section transition
    (100.0, 2.0),   # Narrow neck
    (length, 0.0)   # Sharp tip
]

# Create the solid geometry
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)                          # Start at the center of the base
    .lineTo(0, base_radius)                # Draw the radius to the rim
    .spline(profile_points, includeCurrent=True) # Create the smooth organic curve to the tip
    .close()                               # Close the profile face along the axis
    .revolve(360, (0, 0, 0), (1, 0, 0))    # Revolve around the X-axis to create the solid
)