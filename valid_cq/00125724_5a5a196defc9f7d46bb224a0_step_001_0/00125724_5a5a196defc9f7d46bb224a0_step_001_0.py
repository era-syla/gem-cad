import cadquery as cq

# Parametric dimensions for the cylinder
length = 100.0
radius = 15.0

# Create the cylinder geometry
# We start on the XY plane, draw a circle with the specified radius,
# and extrude it to the specified length to form a solid cylinder.
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)