import cadquery as cq

# Dimensions
outer_diameter = 30.0  # Outer diameter of the washer
inner_diameter = 22.0  # Inner diameter of the hole
thickness = 2.0        # Thickness of the washer

# Create the washer geometry
# We draw two concentric circles on the XY plane and extrude the region between them
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)  # Outer circle
    .circle(inner_diameter / 2.0)  # Inner circle (hole)
    .extrude(thickness)
)