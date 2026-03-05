import cadquery as cq

# Parametric dimensions
length = 200.0   # Length of the cylinder
diameter = 12.0  # Diameter of the cylinder

# Create the cylindrical rod
# 1. Start on the XY plane
# 2. Draw a circle representing the cross-section
# 3. Extrude the circle to the specified length
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)