import cadquery as cq

# Parametric definitions
length = 100.0  # Length of the rod
diameter = 10.0  # Diameter of the rod
radius = diameter / 2.0

# Create a solid cylinder
# We start a Workplane on the XY plane and extrude a circle
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)