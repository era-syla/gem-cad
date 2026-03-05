import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Diameter of the cylinder
thickness = 10.0 # Height/thickness of the cylinder

# Create the cylindrical disc
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(thickness)
)