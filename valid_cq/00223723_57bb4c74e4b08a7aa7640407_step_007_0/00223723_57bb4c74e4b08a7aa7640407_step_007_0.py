import cadquery as cq

# Parametric dimensions
rod_length = 100.0  # Length of the rod
rod_diameter = 2.0  # Diameter of the rod

# Create the 3D model
# 1. Start on the XY plane
# 2. Draw a circle representing the cross-section
# 3. Extrude the circle to create the cylinder
result = (
    cq.Workplane("XY")
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)