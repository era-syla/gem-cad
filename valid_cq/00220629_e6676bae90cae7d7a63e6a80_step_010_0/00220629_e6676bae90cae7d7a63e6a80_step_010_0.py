import cadquery as cq

# Parametric dimensions
outer_diameter = 30.0
inner_diameter = 20.0
thickness = 3.0

# Create the washer geometry
# We draw two circles on the XY plane and extrude the region between them
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)  # Outer boundary
    .circle(inner_diameter / 2.0)  # Inner hole
    .extrude(thickness)            # Create solid
)