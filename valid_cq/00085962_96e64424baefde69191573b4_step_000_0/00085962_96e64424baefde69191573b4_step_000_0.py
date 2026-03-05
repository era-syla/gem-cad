import cadquery as cq

# Parametric dimensions based on visual estimation
base_diameter = 20.0
base_height = 35.0
top_diameter = 13.0
top_height = 20.0

# Create the stepped cylinder geometry
# 1. Start with the base cylinder on the XY plane
# 2. Select the top face (positive Z direction)
# 3. Create a workplane on that face and extrude the smaller cylinder
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_height)
    .faces(">Z")
    .workplane()
    .circle(top_diameter / 2.0)
    .extrude(top_height)
)