import cadquery as cq

# Parameters
height = 60.0
outer_diameter = 18.0
inner_diameter = 12.0

# Create the 3D model
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(height)
)