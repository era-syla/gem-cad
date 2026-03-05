import cadquery as cq

# Parametric dimensions
length = 100.0  # Total length of the rod
diameter = 10.0 # Diameter of the rod
radius = diameter / 2.0

# Create the cylindrical geometry
# We start on the XY plane, draw a circle, and extrude it to the specified length
result = cq.Workplane("XY").circle(radius).extrude(length)