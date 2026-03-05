import cadquery as cq

# Parametric dimensions for the rod
length = 200.0  # Length of the rod
diameter = 4.0  # Diameter of the rod

# Create the cylindrical rod geometry
# 1. Start a workplane on the XY plane
# 2. Draw a circle with the specified radius
# 3. Extrude the circle to create the rod
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)