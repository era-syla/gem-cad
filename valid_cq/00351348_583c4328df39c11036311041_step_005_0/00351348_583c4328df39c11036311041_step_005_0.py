import cadquery as cq

# Parametric dimensions
length = 50.0   # Length of the cylinder
diameter = 10.0 # Diameter of the cylinder

# Create the 3D model
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)