import cadquery as cq

# Parametric dimensions for the rod
length = 200.0  # Total length of the rod
diameter = 4.0  # Diameter of the circular cross-section

# Create the cylindrical rod geometry
# 1. Select the XY workplane
# 2. Draw a circle with the specified radius
# 3. Extrude the circle to the specified length
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)