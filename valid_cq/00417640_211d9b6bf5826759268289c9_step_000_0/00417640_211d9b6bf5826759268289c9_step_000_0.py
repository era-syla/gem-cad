import cadquery as cq

# Parametric dimensions based on the visual proportions
radius = 40.0
thickness = 10.0

# Create the cylindrical disk
# 1. Initialize a workplane on the XY plane
# 2. Draw a circle with the specified radius
# 3. Extrude the circle to the specified thickness
result = cq.Workplane("XY").circle(radius).extrude(thickness)