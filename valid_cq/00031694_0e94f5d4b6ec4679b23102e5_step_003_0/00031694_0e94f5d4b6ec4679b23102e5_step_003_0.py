import cadquery as cq

# Parametric dimensions
length = 150.0   # Length of the rod
diameter = 6.0   # Diameter of the rod

# Generate the geometry
# Create a circle on the XY plane and extrude it to form a cylinder/rod
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)