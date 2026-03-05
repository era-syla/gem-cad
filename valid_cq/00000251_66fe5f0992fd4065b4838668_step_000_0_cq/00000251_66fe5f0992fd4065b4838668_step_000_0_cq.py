import cadquery as cq

# Parametric dimensions for the rod
length = 100.0  # Length of the rod
diameter = 2.0  # Diameter of the rod

# Create the cylindrical rod
# We use Workplane("XY") to start on the XY plane, draw a circle, and extrude it.
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)

# Alternatively, a cylinder primitive could be used:
# result = cq.Workplane("XY").cylinder(length, diameter / 2.0, centered=(True, True, False))