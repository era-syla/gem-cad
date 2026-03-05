import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Diameter of the cylinder
thickness = 5.0  # Thickness of the cylinder

# Create the cylinder (disk)
# We draw a circle on the XY plane and extrude it
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(thickness)
)

# Alternatively, using the primitive cylinder method:
# result = cq.Workplane("XY").cylinder(thickness, diameter / 2.0)