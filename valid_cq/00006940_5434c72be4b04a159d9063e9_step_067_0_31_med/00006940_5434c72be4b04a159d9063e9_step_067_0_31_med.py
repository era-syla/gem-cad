import cadquery as cq

# Parameters
outer_diameter = 20.0
inner_diameter = 14.0
height = 100.0

# Create the tube
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(height)
)