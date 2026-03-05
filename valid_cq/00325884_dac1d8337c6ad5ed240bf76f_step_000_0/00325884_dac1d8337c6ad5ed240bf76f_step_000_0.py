import cadquery as cq

# Define parametric dimensions
radius = 10.0
height = 50.0

# Create the cylinder
# We start on the XY plane, draw a circle, and extrude it upwards
result = cq.Workplane("XY").circle(radius).extrude(height)