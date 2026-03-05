import cadquery as cq

# Parametric dimensions
length = 100.0   # Length of the rod
diameter = 4.0   # Diameter of the rod

# Create the cylindrical geometry
# We define a circle on the XY plane and extrude it along the Z axis
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)