import cadquery as cq

# Parametric dimensions for the washer
outer_diameter = 20.0  # Outer diameter of the washer
inner_diameter = 10.0  # Inner hole diameter
thickness = 2.0        # Thickness of the washer

# Validate parameters to ensure a valid solid
if inner_diameter >= outer_diameter:
    raise ValueError("Inner diameter must be smaller than outer diameter")

# Create the washer geometry
# Method: Sketch two circles and extrude the difference
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)