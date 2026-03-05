import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0
inner_diameter = 36.0
thickness = 6.0

# Generate the washer/ring geometry
# 1. Select the XY workplane
# 2. Draw the outer circle
# 3. Draw the inner circle (this creates the hole when extruded)
# 4. Extrude to the specified thickness
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)