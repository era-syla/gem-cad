import cadquery as cq

# Parametric dimensions for the washer
outer_diameter = 20.0  # The outer diameter of the ring
inner_diameter = 10.0  # The diameter of the inner hole
thickness = 2.0        # The thickness of the washer

# Create the washer geometry
# 1. Initialize workplane on XY axis
# 2. Draw the outer circle
# 3. Draw the inner circle (CadQuery automatically handles the nested profile as a void)
# 4. Extrude the resulting annulus to the specified thickness
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)