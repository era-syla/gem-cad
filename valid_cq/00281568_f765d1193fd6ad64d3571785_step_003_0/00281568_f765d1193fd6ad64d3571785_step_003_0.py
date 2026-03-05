import cadquery as cq

# Parametric dimensions based on the visual proportions
base_diameter = 20.0
base_height = 40.0
top_diameter = 18.0
top_height = 35.0

# Generate the 3D model
# 1. Create the bottom cylinder base
# 2. Select the top face of the base
# 3. Create the top cylinder extrusion
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_height)
    .faces(">Z")
    .workplane()
    .circle(top_diameter / 2.0)
    .extrude(top_height)
)