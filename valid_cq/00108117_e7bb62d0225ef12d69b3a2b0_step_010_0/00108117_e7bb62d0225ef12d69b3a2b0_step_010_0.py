import cadquery as cq

# Parametric dimensions
rod_length = 200.0
rod_diameter = 2.0

# Create a simple cylindrical rod based on the provided image
result = (
    cq.Workplane("XY")
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)