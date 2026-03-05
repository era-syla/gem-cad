import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 200.0   # Total length of the rod
diameter = 10.0  # Diameter of the rod

# Create the 3D cylinder model
# Start on the XY plane, draw the cross-section (circle), and extrude
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)