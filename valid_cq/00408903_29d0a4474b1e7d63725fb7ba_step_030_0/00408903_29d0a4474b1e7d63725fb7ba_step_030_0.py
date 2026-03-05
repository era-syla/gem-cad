import cadquery as cq

# Parametric dimensions
height = 150.0        # Total length of the tube
outer_diameter = 10.0 # External diameter
inner_diameter = 5.0  # Internal diameter (bore)

# Create the hollow cylindrical geometry
# 1. Start a workplane on XY (bottom)
# 2. Draw the outer circle
# 3. Draw the inner circle to form a ring profile
# 4. Extrude to the specified height
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(height)
)