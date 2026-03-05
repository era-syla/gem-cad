import cadquery as cq

# Parameters
outer_diameter = 10.0
inner_diameter = 6.0
height = 40.0

# Create the hollow cylinder (tube)
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(height)
)