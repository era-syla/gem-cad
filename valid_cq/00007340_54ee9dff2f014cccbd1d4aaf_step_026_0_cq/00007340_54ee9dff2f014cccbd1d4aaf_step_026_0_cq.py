import cadquery as cq

# Parameters
outer_diameter = 50.0  # Diameter of the main cylinder
height = 40.0         # Height of the cylinder
hole_diameter = 15.0  # Diameter of the central hole

# Generate the model
# 1. Create a cylinder for the outer body
# 2. Cut a hole through the center in the Z direction
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(height)
    .faces(">Z")
    .hole(hole_diameter)
)