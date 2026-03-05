import cadquery as cq

# Parametric dimensions
base_diameter = 20.0
base_height = 40.0
shaft_diameter = 4.0
shaft_height = 50.0

# Generate the model
# 1. Create the base cylinder
# 2. Select the top face of the base
# 3. Draw and extrude the shaft from the top face
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_height)
    .faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_height)
)