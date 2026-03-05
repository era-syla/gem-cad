import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0
inner_diameter = 45.0
thickness = 1.0

# Create the ring geometry
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)