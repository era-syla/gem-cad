import cadquery as cq

# Parameters for the rod/wire
length = 100.0   # Total length of the rod
diameter = 2.0   # Diameter of the rod

# Create the cylindrical rod
# We create a circle on the XY plane and extrude it along the Z axis
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)

# Alternatively, just using the cylinder primitive could work too:
# result = cq.Workplane("XY").cylinder(length, diameter / 2.0)