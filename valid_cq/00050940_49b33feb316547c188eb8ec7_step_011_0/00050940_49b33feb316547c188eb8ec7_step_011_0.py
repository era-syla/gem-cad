import cadquery as cq

# Define parametric dimensions
length = 60.0          # Total length of the cylinder
outer_diameter = 25.0  # Outer diameter of the cylinder
inner_diameter = 8.0   # Diameter of the central hole

# Create the geometry
# 1. Start on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle (which creates the hole when extruded)
# 4. Extrude to the specified length
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(length)
)