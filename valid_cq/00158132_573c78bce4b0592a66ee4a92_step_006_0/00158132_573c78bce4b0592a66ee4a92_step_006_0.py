import cadquery as cq

# Define parametric dimensions
length = 100.0
diameter = 20.0
radius = diameter / 2.0

# Create the cylinder
# Start on the XY plane, draw a circle of the specified radius, and extrude it to the specified length
result = cq.Workplane("XY").circle(radius).extrude(length)