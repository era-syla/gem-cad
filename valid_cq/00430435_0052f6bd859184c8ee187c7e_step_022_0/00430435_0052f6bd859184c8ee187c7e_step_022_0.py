import cadquery as cq

# Parametric dimensions
height = 60.0        # Total height of the cylinder
outer_diameter = 20.0 # Diameter of the outer cylinder
inner_diameter = 8.0  # Diameter of the through-hole

# Create the hollow cylinder model
# 1. Create a workplane on XY
# 2. Draw the outer circle
# 3. Draw the inner circle to form the ring profile
# 4. Extrude the profile to the desired height
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(height)
)