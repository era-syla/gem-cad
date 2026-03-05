import cadquery as cq

# Define the thickness of the plate
thickness = 2.0

# Define control points for the organic kidney/bean shape
# The shape is drawn using a spline starting from the left tip 
# and tracing the perimeter counter-clockwise.
start_point = (-45, -5)

points = [
    (-15, -25),  # Bottom convex belly
    (35, -20),   # Bottom right curve
    (60, 15),    # Right tip (larger lobe)
    (30, 35),    # Top right lobe
    (0, 15),     # Top concave indentation ("dip")
    (-30, 10),   # Top left curve
    start_point  # Loop back to start for a smooth curve
]

# Create the 3D model
result = (
    cq.Workplane("XY")
    .moveTo(start_point[0], start_point[1])
    .spline(points, includeCurrent=True)
    .close()
    .extrude(thickness)
)