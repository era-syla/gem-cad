import cadquery as cq

# Parametric dimensions
outer_diameter = 20.0  # Diameter of the outer cylinder
inner_diameter = 8.0   # Diameter of the inner through-hole
length = 30.0          # Length of the cylinder

# Create the cylinder with a through hole
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(length)
)