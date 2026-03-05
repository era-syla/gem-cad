import cadquery as cq

# Geometric parameters
diameter = 10.0
height = 50.0

# Create the cylindrical rod
# Start on the XY plane, draw a circle, and extrude it to create the cylinder
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(height)
)