import cadquery as cq

# Geometric parameters
length = 100.0  # Length of the rod
diameter = 2.0  # Diameter of the rod
radius = diameter / 2.0

# Create the cylindrical rod
# We start on the XY plane, draw the circular profile, and extrude it
result = cq.Workplane("XY").circle(radius).extrude(length)