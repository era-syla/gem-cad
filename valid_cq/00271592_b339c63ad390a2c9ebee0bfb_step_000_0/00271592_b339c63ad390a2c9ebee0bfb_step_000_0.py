import cadquery as cq

# Parametric dimensions
length = 500.0  # Length of the rod
radius = 3.0    # Radius of the rod

# Create the solid cylinder (rod)
# Draw a circle on the XY plane and extrude it to the specified length
result = cq.Workplane("XY").circle(radius).extrude(length)