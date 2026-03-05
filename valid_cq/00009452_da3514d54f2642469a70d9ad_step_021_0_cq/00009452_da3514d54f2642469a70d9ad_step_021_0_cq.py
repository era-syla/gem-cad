import cadquery as cq

# Define parameters for the washer
outer_diameter = 20.0
inner_diameter = 8.0
thickness = 2.0

# Create the washer geometry
# 1. Start a workplane (XY plane)
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude the sketch to create the solid with a hole
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)