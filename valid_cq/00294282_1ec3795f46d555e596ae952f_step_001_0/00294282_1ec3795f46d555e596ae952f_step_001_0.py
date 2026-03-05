import cadquery as cq

# Define parametric dimensions
height = 60.0       # Height of the vertical edge
base_width = 30.0   # Width of the bottom edge
top_width = 10.0    # Width of the top edge
thickness = 5.0     # Thickness of the part

# Create the 3D model
# We draw the trapezoidal profile on the XY plane and extrude it
result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),                 # Bottom-left corner
        (base_width, 0),        # Bottom-right corner
        (top_width, height),    # Top-right corner
        (0, height)             # Top-left corner
    ])
    .close()
    .extrude(thickness)
)