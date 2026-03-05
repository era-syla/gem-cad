import cadquery as cq

# Define parametric dimensions
length = 60.0  # Length of the cylinder
radius = 10.0  # Radius of the cylinder

# Create the cylinder
# 1. Start on the XY plane
# 2. Draw a circle of the given radius
# 3. Extrude the circle to the given length to create a solid cylinder
result = cq.Workplane("XY").circle(radius).extrude(length)