import cadquery as cq

# Parametric dimensions
length = 50.0  # Height of the rod
radius = 1.5   # Radius of the rod

# Create a simple cylinder by drawing a circle on the XY plane and extruding it
result = cq.Workplane("XY").circle(radius).extrude(length)