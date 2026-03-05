import cadquery as cq

# Parameters for the L-profile (Angle Iron)
length = 600.0      # Total length of the bar
leg_width = 40.0    # Width of the first leg
leg_height = 40.0   # Width of the second leg
thickness = 4.0     # Wall thickness

# Create the L-shaped cross-section and extrude it
result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),                  # Outer corner
        (leg_width, 0),          # End of leg 1 outer
        (leg_width, thickness),  # End of leg 1 inner
        (thickness, thickness),  # Inner corner
        (thickness, leg_height), # End of leg 2 inner
        (0, leg_height),         # End of leg 2 outer
        (0, 0)                   # Close shape
    ])
    .close()
    .extrude(length)
)