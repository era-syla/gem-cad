import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the rod
diameter = 8.0  # Diameter of the rod

# Create the cylindrical rod
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)