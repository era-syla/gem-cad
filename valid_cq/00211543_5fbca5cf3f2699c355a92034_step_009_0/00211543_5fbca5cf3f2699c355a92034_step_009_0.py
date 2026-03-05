import cadquery as cq

# Parametric dimensions
radius = 50.0

# Create the circular geometry (Wire) on the XY plane
# The image shows a closed loop curve, interpreted here as a simple circle.
result = cq.Workplane("XY").circle(radius)