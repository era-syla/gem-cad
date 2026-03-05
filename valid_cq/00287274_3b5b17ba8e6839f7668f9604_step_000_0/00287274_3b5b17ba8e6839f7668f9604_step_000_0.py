import cadquery as cq

# Parametric dimensions for the stepped pin/shaft
head_diameter = 6.0
head_length = 15.0
shaft_diameter = 3.0
shaft_length = 65.0

# Create the model starting with the thicker head section
result = (
    cq.Workplane("XY")
    .circle(head_diameter / 2.0)
    .extrude(head_length)
    .faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)