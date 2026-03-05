import cadquery as cq

# Parameters for the cylinder dimensions
diameter = 100.0  # Diameter of the cylinder
thickness = 20.0  # Height/thickness of the cylinder

# Create the cylindrical disk
# We start a workplane on the XY plane
# Draw a circle with the specified radius (diameter / 2)
# Extrude it by the specified thickness
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(thickness)
)