import cadquery as cq

# Parametric dimensions
rod_length = 100.0
rod_radius = 5.0

# Create the cylindrical rod
# 1. Start on the XY plane
# 2. Draw a circle with the specified radius
# 3. Extrude it to the specified length to create a solid cylinder
result = cq.Workplane("XY").circle(rod_radius).extrude(rod_length)