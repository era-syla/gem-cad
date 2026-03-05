import cadquery as cq

# Define parametric dimensions
outer_diameter = 50.0  # Overall diameter of the washer
inner_diameter = 20.0  # Diameter of the central hole
thickness = 5.0        # Thickness of the washer
fillet_radius = 1.5    # Radius for the rounded edges

# Create the base washer shape
# 1. Start with a workplane
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude to create the solid ring
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)

# Apply fillets to all edges to get the rounded look
# The image shows rounding on both the top and bottom faces, 
# and both inner and outer edges.
result = result.edges().fillet(fillet_radius)