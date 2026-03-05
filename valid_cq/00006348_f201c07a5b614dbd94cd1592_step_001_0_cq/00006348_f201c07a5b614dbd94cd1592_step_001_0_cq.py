import cadquery as cq

# Parametric dimensions for a standard flat washer
outer_diameter = 20.0
inner_diameter = 10.0
thickness = 2.0

# Create the washer
# 1. Start with a workplane (XY plane)
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude the sketch to the specified thickness
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)