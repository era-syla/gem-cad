import cadquery as cq

# Define parametric dimensions
length = 60.0  # Length of the base along the slope direction
width = 40.0   # Width of the object
height = 20.0  # Vertical height at the back face

# Create the wedge shape
# Strategy: Sketch the triangular profile on the XZ plane (side view) 
# and extrude it along the Y axis (width).
result = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (length, 0), (length, height)])
    .close()
    .extrude(width)
)