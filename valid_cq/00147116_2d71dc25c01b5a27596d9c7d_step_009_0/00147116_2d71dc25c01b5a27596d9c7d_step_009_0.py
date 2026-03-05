import cadquery as cq

# Parametric dimensions
radius = 10.0
height = 30.0

# Create the cylinder
result = cq.Workplane("XY").circle(radius).extrude(height)