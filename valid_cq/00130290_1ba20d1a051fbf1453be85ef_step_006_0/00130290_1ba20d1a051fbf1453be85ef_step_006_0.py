import cadquery as cq

# Define parametric dimensions based on visual estimation of the image
end_cap_diameter = 12.0
end_cap_length = 15.0
shaft_diameter = 5.0
shaft_length = 70.0

# Generate the 3D model using a sequential extrusion process
# 1. Create the first cylindrical end cap on the XY plane
# 2. Select the top face and extrude the thinner central shaft
# 3. Select the top face of the shaft and extrude the second cylindrical end cap
result = (
    cq.Workplane("XY")
    .circle(end_cap_diameter / 2.0)
    .extrude(end_cap_length)
    .faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
    .faces(">Z")
    .workplane()
    .circle(end_cap_diameter / 2.0)
    .extrude(end_cap_length)
)