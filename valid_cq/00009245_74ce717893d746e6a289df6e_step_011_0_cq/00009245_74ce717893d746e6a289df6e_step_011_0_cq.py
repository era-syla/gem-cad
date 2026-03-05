import cadquery as cq

# Parametric dimensions for a standard washer
# These values can be adjusted to change the size of the washer
outer_diameter = 20.0  # Diameter of the outer circle
inner_diameter = 10.0  # Diameter of the inner hole
thickness = 2.0        # Thickness of the washer

# Create the washer geometry
# 1. Start with a workplane (XY plane is standard)
# 2. Draw the outer circle
# 3. Draw the inner circle inside the outer one
# 4. Extrude the sketch to the specified thickness
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)