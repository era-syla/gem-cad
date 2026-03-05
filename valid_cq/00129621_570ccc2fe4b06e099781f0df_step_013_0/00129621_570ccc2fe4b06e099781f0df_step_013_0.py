import cadquery as cq

# Parametric dimensions
outer_diameter = 60.0  # Outer diameter of the disk
inner_diameter = 20.0  # Diameter of the center hole
thickness = 5.0        # Thickness of the part

# Create the model
# 1. Create a workplane on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle (creating a hollow profile)
# 4. Extrude the profile to the specified thickness
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)