import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the cylinder
diameter = 15.0 # Diameter of the cylinder
radius = diameter / 2.0

# Create the solid cylinder
result = cq.Workplane("XY").circle(radius).extrude(length)