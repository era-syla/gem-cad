import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the rod
diameter = 2.0  # Diameter of the rod
radius = diameter / 2.0

# Create the cylindrical rod
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)