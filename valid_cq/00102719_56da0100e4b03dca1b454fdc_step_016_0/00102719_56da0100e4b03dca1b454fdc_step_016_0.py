import cadquery as cq

# Define parametric dimensions
length = 300.0  # Length of the rod
diameter = 10.0  # Diameter of the rod

# Create the cylindrical rod
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)