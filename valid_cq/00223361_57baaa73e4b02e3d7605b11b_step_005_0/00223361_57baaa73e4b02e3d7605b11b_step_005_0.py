import cadquery as cq

# Parametric dimensions
length = 50.0   # Length of the cylinder
radius = 5.0    # Radius of the cylinder

# Create the cylinder using the Workplane API
# 1. Select the XY plane
# 2. Draw a circle with the specified radius
# 3. Extrude the circle to the specified length to create a solid cylinder
result = cq.Workplane("XY").circle(radius).extrude(length)