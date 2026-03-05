import cadquery as cq

# Geometric parameters for the cylinder
radius = 5.0
length = 30.0

# Create the 3D model
# 1. Start a workplane on the XY plane
# 2. Draw a circle with the specified radius
# 3. Extrude the circle to create the cylinder
result = cq.Workplane("XY").circle(radius).extrude(length)