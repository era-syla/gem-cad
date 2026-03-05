import cadquery as cq

# Main body and tip
main = (
    cq.Workplane("XZ")
    .polyline([(0, 0), (1.5, 5), (4, 20), (4, 110), (5, 115), (5, 120), (0, 120)])
    .close()
    .revolve(360)
)

# Click button at rear
button = (
    cq.Workplane("XY")
    .workplane(offset=110)
    .circle(5)
    .extrude(5)
)

# Clip on the side
clip = (
    cq.Workplane("YZ", origin=(5, 0, 60))
    .rect(8, 30)
    .extrude(-1)
)

result = main.union(button).union(clip)