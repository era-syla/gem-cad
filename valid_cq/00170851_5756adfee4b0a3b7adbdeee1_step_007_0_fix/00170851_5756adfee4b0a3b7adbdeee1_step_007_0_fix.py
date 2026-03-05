import cadquery as cq

# Main body
main = (
    cq.Workplane("XY")
    .box(80, 20, 10)
    .faces(">Z")
    .workplane()
    .rect(70, 10)
    .cutBlind(-6)
    .faces(">Y")
    .workplane(centerOption="CenterOfBoundBox")
    .polyline([(-40, 5), (0, 2), (40, 5)])
    .close()
    .cutBlind(-10)
)

# Tail section
tail = (
    cq.Workplane("XY")
    .transformed(offset=(55, 0, 0))
    .box(30, 15, 8)
)

# Wedge feature on the end
wedge = (
    cq.Workplane("YZ")
    .transformed(offset=(85, 0, 10))
    .polyline([(-7.5, 0), (0, 3), (7.5, 0)])
    .close()
    .extrude(30)
)

result = main.union(tail).union(wedge)