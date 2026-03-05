import cadquery as cq

# Define parametric dimensions
diameter = 50.0  # Diameter of the disc
thickness = 2.0  # Thickness of the disc

# Create the disc geometry
# We sketch a circle on the XY plane and extrude it
result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(thickness)
)