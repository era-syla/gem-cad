import cadquery as cq

# Parameters
length = 50.0  # Length of the cylinder
diameter = 10.0  # Diameter of the cylinder

# Create the solid cylinder
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)