import cadquery as cq

# Parametric dimensions
outer_diameter = 20.0  # Diameter of the outer cylinder
inner_diameter = 10.0  # Diameter of the inner hole
length = 40.0         # Length of the tube

# Create the model
# 1. Start with a workplane (XY plane)
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude the sketch to create the tube shape
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(length)
)