import cadquery as cq

# Parametric dimensions
outer_diameter = 30.0
inner_diameter = 15.0
thickness = 4.0

# Create the washer geometry
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)