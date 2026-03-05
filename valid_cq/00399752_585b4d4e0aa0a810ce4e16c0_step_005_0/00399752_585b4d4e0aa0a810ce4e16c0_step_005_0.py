import cadquery as cq

# Parametric dimensions based on the visual aspect ratio
length = 50.0
diameter = 10.0
radius = diameter / 2.0

# Create the cylindrical rod
# 1. Define a Workplane (XY plane)
# 2. Draw a circle with the specified radius
# 3. Extrude the circle to create a solid cylinder
result = cq.Workplane("XY").circle(radius).extrude(length)