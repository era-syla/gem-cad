import cadquery as cq

outer = [(20, 0), (10, 20), (-10, 0), (10, -20)]
inner = [(x * 0.7, y * 0.7) for x, y in outer]

result = (
    cq.Workplane("XY")
    .spline(outer)
    .close()
    .extrude(10)
    .edges("|Z").fillet(2)
    .faces(">Z")
    .workplane()
    .spline(inner)
    .close()
    .cutBlind(-2)
    .faces(">Z")
    .workplane()
    .polygon(5, 16)
    .cutThruAll()
)