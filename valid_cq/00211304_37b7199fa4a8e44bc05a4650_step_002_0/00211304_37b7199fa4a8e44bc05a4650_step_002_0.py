import cadquery as cq

# Geometric parameters
length = 80.0       # Total length of the wedge
width_wide = 35.0   # Width at the larger end
width_narrow = 15.0 # Width at the smaller end
thickness = 10.0    # Thickness (extrusion height)

# Define vertices for the trapezoidal base profile
# Coordinates are (x, y) relative to the workplane origin
# Ordered counter-clockwise
points = [
    (0, -width_wide / 2.0),      # Bottom-left
    (length, -width_narrow / 2.0), # Bottom-right
    (length, width_narrow / 2.0),  # Top-right
    (0, width_wide / 2.0)        # Top-left
]

# Create the 3D model
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)