import cadquery as cq

# Parametric dimensions for the rod
length = 150.0
diameter = 8.0
radius = diameter / 2.0

# Create the cylindrical rod
# 1. Start a workplane on the XY plane
# 2. Draw a circle with the specified radius
# 3. Extrude the circle to the specified length to create a solid cylinder
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)