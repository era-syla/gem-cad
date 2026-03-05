import cadquery as cq

# Define parametric dimensions
cylinder_radius = 20.0  # Radius of the cylinder
cylinder_height = 50.0  # Height of the cylinder

# Create the cylinder using CadQuery
# We draw a circle on the XY plane and extrude it
result = (
    cq.Workplane("XY")
    .circle(cylinder_radius)
    .extrude(cylinder_height)
)

# Alternatively, using the cylinder primitive directly which is often more concise
# result = cq.Workplane("XY").cylinder(cylinder_height, cylinder_radius)