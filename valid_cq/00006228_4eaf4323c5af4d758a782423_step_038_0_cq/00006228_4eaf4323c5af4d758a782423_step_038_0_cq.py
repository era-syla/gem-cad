import cadquery as cq

# Parametric Dimensions
base_length = 50.0  # Length along the X axis
base_width = 10.0   # Width/Thickness along the Y axis
height = 50.0       # Height along the Z axis
fillet_radius = 1.0 # Radius for rounding edges

# Create the basic triangular prism shape
# We draw a right triangle on the XZ plane and extrude it along Y
result = (
    cq.Workplane("XY")
    .polyline([(0, 0), (base_length, 0), (0, height), (0, 0)])
    .close()
    .extrude(base_width)
)

# Apply fillets to all edges to match the smooth look in the image
# The image shows rounding on almost every visible edge
result = result.edges().fillet(fillet_radius)