import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Diameter of the cylinder
height = 10.0    # Height (thickness) of the cylinder

# Create the cylindrical disk
# We draw a circle on the XY plane and extrude it
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(height)
)

# Alternatively, using the simpler Cylinder primitive:
# result = cq.Workplane("XY").cylinder(height, diameter / 2.0)