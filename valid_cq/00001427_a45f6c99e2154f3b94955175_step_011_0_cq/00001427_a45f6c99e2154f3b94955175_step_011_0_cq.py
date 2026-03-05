import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0  # Outer diameter of the washer
inner_diameter = 30.0  # Inner diameter of the hole
thickness = 2.0        # Thickness of the washer

# Create the washer
# Method: Create a cylinder for the outer diameter, then cut the inner hole
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)