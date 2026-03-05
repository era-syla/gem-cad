import cadquery as cq

length = 100
height = 40
depth = 30
step = 20
lower_length = 60

result = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (lower_length, 0),
        (lower_length, step),
        (step, step),
        (step, height),
        (length, height),
        (length, 0)
    ])
    .close()
    .extrude(depth)
)