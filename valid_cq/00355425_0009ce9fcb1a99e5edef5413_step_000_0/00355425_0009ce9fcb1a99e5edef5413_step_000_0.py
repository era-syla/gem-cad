import cadquery as cq

# Parametric dimensions
cylinder_diameter = 10.0
cylinder_height = 60.0

# Create the cylinder
# 1. Start on the XY plane
# 2. Draw a circle with the specified radius
# 3. Extrude to the specified height
result = (
    cq.Workplane("XY")
    .circle(cylinder_diameter / 2.0)
    .extrude(cylinder_height)
)