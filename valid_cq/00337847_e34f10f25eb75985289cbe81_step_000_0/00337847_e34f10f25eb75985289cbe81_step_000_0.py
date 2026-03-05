import cadquery as cq

# Define parametric dimensions
length = 50.0  # Length of the base
height = 40.0  # Height of the vertical side
width = 30.0   # Thickness of the wedge

# Generate the wedge geometry
# We draw the triangular profile on the XZ plane and extrude it along the Y axis
result = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (length, 0), (0, height)])
    .close()
    .extrude(width)
)