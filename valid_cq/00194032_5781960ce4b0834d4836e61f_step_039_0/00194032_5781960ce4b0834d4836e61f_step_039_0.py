import cadquery as cq

# Parametric dimensions
base_diameter = 20.0
base_length = 40.0
tip_diameter = 13.0
tip_length = 20.0

# Generate the stepped cylinder model
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_length)
    .faces(">Z")
    .workplane()
    .circle(tip_diameter / 2.0)
    .extrude(tip_length)
)