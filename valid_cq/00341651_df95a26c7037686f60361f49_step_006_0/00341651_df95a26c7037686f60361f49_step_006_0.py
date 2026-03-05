import cadquery as cq

# Geometric parameters for the rod
length = 100.0   # Total length of the rod
diameter = 5.0   # Diameter of the rod
radius = diameter / 2.0

# Create the 3D model
# 1. Select the XY plane to start the sketch
# 2. Draw a circle with the specified radius
# 3. Extrude the circle to the specified length to create a cylinder
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)