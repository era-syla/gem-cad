import cadquery as cq

# Define parametric dimensions
diameter = 50.0  # Diameter of the disc
thickness = 2.0  # Thickness of the disc

# Generate the geometry
# Create a workplane, draw a circle, and extrude it to create a disc
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(thickness)
)