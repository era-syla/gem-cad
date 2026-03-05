import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Diameter of the cylinder
height = 40.0    # Height of the cylinder
radius = diameter / 2.0

# Create the solid cylinder
# We draw a circle on the XY plane and extrude it
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(height)
)

# Alternatively, we could specificy it directly as a primitive:
# result = cq.Workplane("XY").cylinder(height, radius)