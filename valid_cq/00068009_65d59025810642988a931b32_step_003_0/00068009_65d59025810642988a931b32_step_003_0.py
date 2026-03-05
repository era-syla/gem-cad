import cadquery as cq

# Parametric dimensions for the rod
length = 300.0  # Total length of the rod
diameter = 10.0 # Diameter of the rod

# Create the 3D model
# 1. Start with a workplane (XY plane)
# 2. Draw a circle representing the cross-section
# 3. Extrude the circle to create the solid rod
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)