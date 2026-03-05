import cadquery as cq

# Dimensions
length = 100.0      # length along X
depth = 20.0        # extrusion depth along Y
height_left = 10.0  # height at X=0
height_right = 50.0 # height at X=length

result = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (length, 0),
        (length, height_right),
        (0, height_left),
    ])
    .close()
    .extrude(depth)
)