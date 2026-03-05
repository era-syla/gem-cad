import cadquery as cq

# Parametric dimensions
radius = 10.0
height = 50.0

# Create the cylinder model
result = cq.Workplane("XY").circle(radius).extrude(height)