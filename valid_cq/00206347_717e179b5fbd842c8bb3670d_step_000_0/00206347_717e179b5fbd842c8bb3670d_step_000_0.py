import cadquery as cq

# Parametric dimensions for the trapezoidal prism
length = 100.0       # Total length of the prism
base_width = 40.0    # Width at the bottom
top_width = 20.0     # Width at the top
height = 15.0        # Vertical height

# Define the points for the trapezoidal cross-section
# The profile is centered on the local origin
# Drawn on the YZ plane to correspond to a side profile
points = [
    (-base_width / 2.0, 0.0),
    (base_width / 2.0, 0.0),
    (top_width / 2.0, height),
    (-top_width / 2.0, height)
]

# Generate the 3D geometry
# - Start on the YZ plane
# - Draw the polyline profile
# - Extrude along the X axis symmetrically
result = (
    cq.Workplane("YZ")
    .polyline(points)
    .close()
    .extrude(length / 2.0, both=True)
)