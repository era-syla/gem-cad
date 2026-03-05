import cadquery as cq

# Parametric dimensions
length = 40.0        # Length of the straight rectangular section
width = 20.0         # Width of the part (also the diameter of the rounded end)
thickness = 15.0     # Thickness (extrusion depth) of the part
hole_diam = 10.0     # Diameter of the through-hole

# Create the 2D profile, extrude, and drill the hole
result = (
    cq.Workplane("XY")
    # Draw the main profile
    .moveTo(0, width / 2.0)
    .lineTo(length, width / 2.0)
    .threePointArc((length + width / 2.0, 0), (length, -width / 2.0))
    .lineTo(0, -width / 2.0)
    .close()
    # Extrude into a 3D solid
    .extrude(thickness)
    # Select the top face and add the hole at the center of the arc
    .faces(">Z")
    .workplane()
    .center(length, 0)
    .hole(hole_diam)
)