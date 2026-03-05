import cadquery as cq

# Parameters
base_length = 20.0
height = 15.0
thickness = 0.5

# Define the points for the right triangle
pts = [
    (0, 0),
    (base_length, 0),
    (0, height)
]

# Create the 3D model
result = (
    cq.Workplane("front")
    .polyline(pts)
    .close()
    .extrude(thickness)
)