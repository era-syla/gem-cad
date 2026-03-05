import cadquery as cq

# Parametric dimensions
leg_width = 30.0      # Width of the legs of the angle iron
thickness = 3.0       # Thickness of the material
length = 300.0        # Length of the extrusion

# Define the points for the L-shaped cross-section
# Starting from the outer corner at (0,0)
pts = [
    (0, 0),
    (leg_width, 0),
    (leg_width, thickness),
    (thickness, thickness),
    (thickness, leg_width),
    (0, leg_width)
]

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(length)
)