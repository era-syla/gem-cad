import cadquery as cq

# Parametric dimensions
cylinder_length = 50.0  # Length of the cylinder
cylinder_radius = 5.0   # Radius of the cylinder

# Create the cylinder
# We construct a workplane (default is XY), draw a circle, and extrude it.
result = (
    cq.Workplane("XY")
    .circle(cylinder_radius)
    .extrude(cylinder_length)
)