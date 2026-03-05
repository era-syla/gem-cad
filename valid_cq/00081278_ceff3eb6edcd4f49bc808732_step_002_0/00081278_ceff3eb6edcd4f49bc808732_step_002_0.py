import cadquery as cq

# Parametric dimensions
length = 100.0         # Total length of the tube
outer_diameter = 20.0  # Outer diameter
wall_thickness = 1.5   # Thickness of the wall

# Calculated dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder (tube)
# 1. Create a workplane
# 2. Draw the outer circle
# 3. Draw the inner circle to define the wall
# 4. Extrude the resulting ring profile
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)