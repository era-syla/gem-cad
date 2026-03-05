import cadquery as cq

# Parametric dimensions
outer_diameter = 40.0
inner_diameter = 12.0
height = 15.0
fillet_radius = 2.0

# Create the base cylinder
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(height)
)

# Create the center hole and fillet the top edge of the hole
result = (
    result.faces(">Z")
    .hole(inner_diameter)
    .edges(cq.selectors.RadiusNthSelector(0)) # Selects the inner hole edge
    .fillet(fillet_radius)
)