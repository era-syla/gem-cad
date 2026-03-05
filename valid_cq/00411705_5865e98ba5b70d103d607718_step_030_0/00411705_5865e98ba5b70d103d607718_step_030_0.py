import cadquery as cq

# Parametric dimensions
rod_length = 50.0
rod_diameter = 1.0

# Create the cylindrical rod
# We start on the XY plane, draw a circle, and extrude it in the Z direction
result = (
    cq.Workplane("XY")
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)