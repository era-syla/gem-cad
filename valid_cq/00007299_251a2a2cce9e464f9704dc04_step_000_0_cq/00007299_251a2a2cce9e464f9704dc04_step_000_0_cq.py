import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0  # Total diameter of the ring
inner_diameter = 35.0  # Diameter of the hole
height = 15.0          # Thickness/height of the ring

# Calculate radii for the circles
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

# Create the ring geometry
# 1. Start a sketch on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude the sketch to create the solid ring
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)