import cadquery as cq

# Geometric parameters
length = 100.0   # Total length of the rod
diameter = 5.0   # Diameter of the rod

# Generate the 3D model
# Create a circle on the XY plane and extrude it to create a solid cylinder
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)