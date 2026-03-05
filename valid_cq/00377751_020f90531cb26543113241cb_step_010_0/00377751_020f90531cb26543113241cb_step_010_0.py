import cadquery as cq

# Parametric dimensions for the rod
length = 500.0      # Total length of the rod
diameter = 8.0      # Diameter of the rod

# Create the solid cylindrical geometry
# We define a circle on the XY plane and extrude it to the specified length
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)