import cadquery as cq

# Parametric dimensions
cylinder_height = 80.0
cylinder_radius = 10.0

# Create the cylinder
result = (
    cq.Workplane("XY")
    .circle(cylinder_radius)
    .extrude(cylinder_height)
)