import cadquery as cq

# Define parametric dimensions
length = 100.0  # Length of the rod
diameter = 5.0  # Diameter of the rod

# Create the cylindrical rod
# We create a workplane, draw a circle, and extrude it
result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(length)
)