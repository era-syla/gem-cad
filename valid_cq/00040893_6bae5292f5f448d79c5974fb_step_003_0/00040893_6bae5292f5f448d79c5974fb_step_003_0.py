import cadquery as cq

# Parametric dimensions
length = 300.0    # Length of the rod
diameter = 10.0   # Diameter of the rod
radius = diameter / 2.0

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)