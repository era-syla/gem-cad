import cadquery as cq

# Geometric parameters
base_radius = 60.0
base_thickness = 1.0
rod_radius = 2.5
rod_height = 40.0

# Create the model
# 1. Start with the XY plane
# 2. Draw the large base circle
# 3. Extrude the base thickness
# 4. Select the top face of the base
# 5. Draw the smaller rod circle on the center
# 6. Extrude the rod height
result = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_thickness)
    .faces(">Z")
    .workplane()
    .circle(rod_radius)
    .extrude(rod_height)
)