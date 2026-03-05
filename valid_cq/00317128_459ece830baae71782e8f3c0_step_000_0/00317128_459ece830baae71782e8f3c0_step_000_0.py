import cadquery as cq

# Parameters defining the trapezoidal plate dimensions
length = 100.0
width_front = 50.0   # Width at the near end
width_back = 90.0    # Width at the far end
thickness = 8.0

# Define the points for the trapezoidal profile
# The shape is centered on the XY plane, widening along the Y axis
points = [
    (-width_front / 2.0, -length / 2.0),  # Front Left
    (width_front / 2.0, -length / 2.0),   # Front Right
    (width_back / 2.0, length / 2.0),     # Back Right
    (-width_back / 2.0, length / 2.0)     # Back Left
]

# Create the 3D model by drawing the profile and extruding it
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(thickness)
)