import cadquery as cq

# Parameters for the stepped pin/shaft
base_diameter = 20.0
base_height = 40.0
top_diameter = 14.0
top_height = 30.0

# Create the base cylinder
result = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_height)
)

# Create the top cylinder on top of the base
result = (
    result.faces(">Z")
    .workplane()
    .circle(top_diameter / 2.0)
    .extrude(top_height)
)