import cadquery as cq

# Parametric dimensions based on visual estimation of the tube
length = 100.0
outer_diameter = 25.0
inner_diameter = 17.0

# Create the hollow cylinder geometry
# 1. Define the workplane (XY plane)
# 2. Draw the outer circle
# 3. Draw the inner circle (defines the hollow part)
# 4. Extrude the resulting profile to create the tube
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(length)
)