import cadquery as cq

# Parametric dimensions for the rod
length = 500.0  # Total length of the rod
diameter = 5.0  # Diameter of the rod

# Create the 3D model
# Start on the XY plane, draw a circle representing the cross-section,
# and extrude it to the specified length.
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)