import cadquery as cq

# Parametric dimensions
outer_diameter = 60.0
wall_thickness = 4.0
height = 12.0

# derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the ring geometry
# We draw the outer circle, then the inner circle on the same workplane.
# CadQuery interprets the inner circle as a hole when extruding.
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)