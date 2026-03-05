import cadquery as cq

# Define parametric dimensions
diameter = 100.0  # Diameter of the disc
thickness = 2.0   # Thickness of the disc (thin plate appearance)

# Create the disc
result = (
    cq.Workplane("XY")
    .circle(diameter / 2)
    .extrude(thickness)
)