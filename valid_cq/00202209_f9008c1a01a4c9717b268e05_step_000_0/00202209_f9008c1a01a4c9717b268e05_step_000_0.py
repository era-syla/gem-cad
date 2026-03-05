import cadquery as cq

# Parameters for the cylinder
height = 60.0
radius = 5.0

# Create the cylinder geometry
# We start on the XY plane, draw a circle, and extrude it upwards along the Z axis
result = cq.Workplane("XY").circle(radius).extrude(height)