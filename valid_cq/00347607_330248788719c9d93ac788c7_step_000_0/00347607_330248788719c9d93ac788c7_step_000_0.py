import cadquery as cq

# Parametric dimensions
length = 100.0  # Total length of the rod
diameter = 6.0  # Diameter of the rod

# Create the cylindrical rod
# 1. Select the XY workplane
# 2. Draw a circle with the specified radius
# 3. Extrude the circle to the specified length to create a solid cylinder
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)