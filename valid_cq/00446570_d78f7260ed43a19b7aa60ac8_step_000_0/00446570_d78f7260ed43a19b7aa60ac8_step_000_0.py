import cadquery as cq

# Model parameters
outer_diameter = 100.0
height = 10.0
wall_thickness = 1.5

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the ring/band geometry
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)