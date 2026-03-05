import cadquery as cq

# Parametric dimensions for the L-profile (Angle Iron)
length = 1000.0  # Total length of the bar
leg1_width = 30.0  # Width of the first leg (horizontal)
leg2_height = 30.0 # Height of the second leg (vertical)
thickness = 3.0    # Thickness of the material

# Create the L-profile sketch
# We draw the cross-section on the XY plane and extrude it along Z
# Origin is at the outer corner of the 'L'
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg1_width, 0)
    .lineTo(leg1_width, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, leg2_height)
    .lineTo(0, leg2_height)
    .close()
    .extrude(length)
)

# Optional: To match the visual orientation better (long axis typically along X or Y)
# let's rotate it so it lies flat
# result = result.rotate((0,0,0), (1,0,0), 90)