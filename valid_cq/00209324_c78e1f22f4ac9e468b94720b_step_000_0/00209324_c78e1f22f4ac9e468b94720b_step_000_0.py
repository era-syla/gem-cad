import cadquery as cq

# Parametric dimensions estimated from the image
height = 80.0
outer_diameter = 40.0
inner_diameter = 24.0

# Create the hollow cylinder (tube)
# Method: Sketch two concentric circles on the XY plane and extrude them.
# The area between the circles forms the solid wall.
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(height)
)