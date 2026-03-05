import cadquery as cq

# Define parametric variables for the cylinder
cylinder_radius = 20.0  # Radius of the cylinder
cylinder_length = 80.0  # Length of the cylinder

# Create the cylinder using CadQuery
# We start a workplane on the XY plane
# Draw a circle with the specified radius
# Extrude it by the specified length
result = (
    cq.Workplane("XY")
    .circle(cylinder_radius)
    .extrude(cylinder_length)
)