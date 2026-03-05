import cadquery as cq

# Parametric dimensions
height = 100.0  # Total length of the rod
diameter = 4.0  # Diameter of the rod

# Create the solid geometry
# Start on the XY plane, draw a circle, and extrude it vertically to form a cylinder
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(height)
)