import cadquery as cq

# Define parametric dimensions
length = 100.0
diameter = 25.0

# Create the cylinder model
# 1. Start a new workplane on the XY plane
# 2. Draw a circle with the specified radius
# 3. Extrude the circle to create the cylinder rod
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)