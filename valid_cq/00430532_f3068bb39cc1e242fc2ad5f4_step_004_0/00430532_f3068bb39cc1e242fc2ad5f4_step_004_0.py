import cadquery as cq

# Define parametric dimensions
length = 50.0       # Length of the cylinder
diameter = 12.0     # Diameter of the cylinder

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)