import cadquery as cq

# Define parameters for the angle iron (L-profile) dimensions
length = 300.0        # Total length of the beam
leg_width = 30.0      # Length of the horizontal leg
leg_height = 30.0     # Length of the vertical leg
thickness = 3.0       # Material thickness

# Create the L-profile on the YZ plane and extrude along the X axis
# This creates a long beam typical of the image provided
result = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(leg_width, 0)
    .lineTo(leg_width, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, leg_height)
    .lineTo(0, leg_height)
    .close()
    .extrude(length)
)