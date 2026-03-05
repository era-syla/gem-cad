import cadquery as cq

# Parameters for the L-angle profile
length = 300.0      # Total length of the bar
leg_size = 20.0     # Width/Height of the L legs
thickness = 3.0     # Material thickness

# Create the L-profile on the YZ plane and extrude along the X axis
result = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(leg_size, 0)               # Bottom outer edge
    .lineTo(leg_size, thickness)       # Bottom leg thickness
    .lineTo(thickness, thickness)      # Inner corner horizontal
    .lineTo(thickness, leg_size)       # Inner corner vertical
    .lineTo(0, leg_size)               # Top leg thickness
    .close()                           # Connect back to origin (0,0)
    .extrude(length)
)