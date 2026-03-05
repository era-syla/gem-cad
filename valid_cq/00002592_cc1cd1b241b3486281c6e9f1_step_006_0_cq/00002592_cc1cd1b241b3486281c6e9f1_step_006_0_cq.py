import cadquery as cq

# Define parametric dimensions
outer_diameter = 20.0
inner_diameter = 8.0
height = 10.0
fillet_radius = 1.0

# Create the base cylindrical shape with a hole
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(height)
)

# Apply a fillet to the top edge of the hole
# Selecting the top face, then the inner edge
result = result.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).fillet(fillet_radius)