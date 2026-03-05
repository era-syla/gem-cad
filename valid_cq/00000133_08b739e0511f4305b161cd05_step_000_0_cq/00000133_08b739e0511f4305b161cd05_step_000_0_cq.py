import cadquery as cq

# Parameters for the washer
outer_diameter = 30.0
inner_diameter = 14.0
thickness = 4.0

# Create the washer
# 1. Start a workplane (XY plane is standard)
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude the sketch to create the 3D solid
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)