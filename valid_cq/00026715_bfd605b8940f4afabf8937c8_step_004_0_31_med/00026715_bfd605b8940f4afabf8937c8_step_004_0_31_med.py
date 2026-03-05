import cadquery as cq

# Parameters for the parametric model
length = 50.0          # Length of the straight rectangular section
width = 30.0           # Overall width of the part (and diameter of the rounded end)
thickness = 20.0       # Extrusion thickness
hole_radius = 7.5      # Radius of the inner through-hole

# Derived parameter
radius = width / 2.0

# Create the part
result = (
    cq.Workplane("XY")
    # Draw the outer profile
    .moveTo(-length, -radius)
    .lineTo(0, -radius)
    .threePointArc((radius, 0), (0, radius))
    .lineTo(-length, radius)
    .close()
    # Draw the inner hole profile
    .circle(hole_radius)
    # Extrude the 2D sketch into a 3D solid
    .extrude(thickness)
)