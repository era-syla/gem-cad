import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0
wall_thickness = 5.0
length = 40.0

# Calculated dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the model
# 1. Start with a 2D workplane
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude the resulting ring to the specified length
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)