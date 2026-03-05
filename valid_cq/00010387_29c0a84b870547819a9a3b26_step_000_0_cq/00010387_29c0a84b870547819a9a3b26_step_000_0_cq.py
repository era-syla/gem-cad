import cadquery as cq

# Parametric dimensions
outer_diameter = 20.0
inner_diameter = 10.0
height = 20.0

# Create the bushing/spacer geometry
# 1. Start with a workplane (XY plane)
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude the sketch to create the solid with a hole
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(height)
)