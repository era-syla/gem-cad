import cadquery as cq

# Parametric dimensions
width = 100.0
height = 100.0
thickness = 5.0

# Create the 3D model
result = (
    cq.Workplane("front")
    .polyline([(0, 0), (width, 0), (0, height)])
    .close()
    .extrude(thickness)
)