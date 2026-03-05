import cadquery as cq

# Parametric dimensions estimated from the image
radius = 5.0
height = 80.0

# Create a simple cylinder based on the primitive shape shown
result = cq.Workplane("XY").circle(radius).extrude(height)