import cadquery as cq

# Parameters for the L-profile
height = 100.0   # Total length/height of the profile
leg1_width = 15.0 # Width of the first leg
leg2_width = 15.0 # Width of the second leg
thickness = 2.0  # Thickness of the material

# Create the L-shape profile sketch
# We draw on the XY plane and then extrude along Z
# Origin will be at the corner of the L
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg1_width, 0)
    .lineTo(leg1_width, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, leg2_width)
    .lineTo(0, leg2_width)
    .close()
    .extrude(height)
)

# Optional: Center the view if exported, though 'result' variable is the requirement
# result = result.translate((-leg1_width/2, -leg2_width/2, -height/2))