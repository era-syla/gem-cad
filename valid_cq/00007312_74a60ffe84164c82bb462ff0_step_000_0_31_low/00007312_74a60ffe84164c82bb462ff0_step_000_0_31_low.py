import cadquery as cq

# Parameters
outer_radius = 5.0
inner_radius = 3.5
height = 30.0

# Create the hollow cylinder
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)