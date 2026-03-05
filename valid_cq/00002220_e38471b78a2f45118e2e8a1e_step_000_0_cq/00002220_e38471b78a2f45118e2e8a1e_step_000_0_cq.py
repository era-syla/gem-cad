import cadquery as cq

# Parametric dimensions
height = 100.0       # Total height of the angle profile
leg_length_1 = 60.0  # Length of the first leg
leg_length_2 = 60.0  # Length of the second leg
thickness = 10.0     # Thickness of the material

# Create the L-shape profile sketch
# We will draw the L-shape on the XY plane and extrude it along Z
# Origin is placed at the outer corner
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_length_1, 0)
    .lineTo(leg_length_1, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, leg_length_2)
    .lineTo(0, leg_length_2)
    .close()
    .extrude(height)
)

# Optional: Center or re-orient if needed, but the current origin 
# at the outer corner bottom is a standard CAD practice.