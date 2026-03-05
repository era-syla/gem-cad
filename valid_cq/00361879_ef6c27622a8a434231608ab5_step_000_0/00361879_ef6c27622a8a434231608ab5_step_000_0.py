import cadquery as cq

# Parametric dimensions for the model
thickness = 5.0       # Thickness of the part (height in Z)
bar_width = 10.0      # Width of the rectangular profile
long_leg_len = 80.0   # Total length of the longer leg
short_leg_len = 35.0  # Total length of the shorter leg

# Create the L-shaped solid
# We draw the 2D profile on the XY plane and extrude it
result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),                        # Outer corner
        (long_leg_len, 0),             # End of long leg
        (long_leg_len, bar_width),     # Width of long leg
        (bar_width, bar_width),        # Inner corner
        (bar_width, short_leg_len),    # End of short leg
        (0, short_leg_len),            # Width of short leg
        (0, 0)                         # Close the loop
    ])
    .close()
    .extrude(thickness)
)