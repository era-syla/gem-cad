import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0  # Diameter of the outer cylinder
inner_diameter = 15.0  # Diameter of the through hole
thickness = 15.0       # Thickness of the disc

# Create the washer/spacer
# 1. Start with a workplane
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude the sketch to create the solid with a hole
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)