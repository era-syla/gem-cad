import cadquery as cq

result = (
    cq.Workplane("XZ")
    .polyline([
        (0, -30),
        (10, -20),
        (20,   0),
        (15,  20),
        (0,   30)
    ])
    .close()
    .revolve(360)
)