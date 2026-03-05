import cadquery as cq

# Parametric dimensions based on the visual estimation of the rectangular tube
length = 800.0
width = 40.0
height = 50.0
wall_thickness = 3.0

# Create the hollow rectangular tube geometry
# 1. Create a workplane on the XY plane
# 2. Draw the outer rectangle
# 3. Draw the inner rectangle to subtract the material (creating the hollow profile)
# 4. Extrude the profile to the specified length
result = (
    cq.Workplane("XY")
    .rect(width, height)
    .rect(width - 2 * wall_thickness, height - 2 * wall_thickness)
    .extrude(length)
)