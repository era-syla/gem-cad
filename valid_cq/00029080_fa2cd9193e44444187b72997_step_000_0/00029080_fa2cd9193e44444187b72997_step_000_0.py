import cadquery as cq

# Parametric dimensions based on the visual proportions
height = 30.0
width = 50.0
thickness = 2.0

# Create the triangular prism
# We draw a right-angled triangle on the XY plane and extrude it
# The vertical edge corresponds to the Y-axis, horizontal to X-axis
result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (0, height), (width, 0)])
    .close()
    .extrude(thickness)
)