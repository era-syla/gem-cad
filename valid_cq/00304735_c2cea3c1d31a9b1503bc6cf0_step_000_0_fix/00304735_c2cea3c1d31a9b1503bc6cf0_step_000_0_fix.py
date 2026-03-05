import cadquery as cq

# Main half-cylinder body
body = (
    cq.Workplane("XY")
    .circle(50)
    .extrude(20)
    .cut(
        cq.Workplane("XY")
        .box(200, 100, 200, centered=(True, False, True))
        .translate((0, -50, 0))
    )
)

# Central mounting plate on flat face
plate = (
    cq.Workplane("XY")
    .box(60, 5, 20, centered=(True, False, False))
    .translate((0, -52.5, 10))
    .faces(">Y")
    .workplane()
    .pushPoints([(-20, 0), (20, 0)])
    .hole(5)
)

# Triangular pockets on curved face
triangle = (
    cq.Workplane("XY")
    .polyline([(-15, 0), (0, 10), (15, 0)])
    .close()
    .extrude(5)
    .translate((0, 45, 5))
)
# Cut two symmetric pockets
body = body.cut(triangle).cut(triangle.mirror("XZ"))

# Small rectangular plug beneath
plug = (
    cq.Workplane("XY")
    .box(5, 5, 5, centered=(True, True, True))
    .translate((0, -52.5, -2.5))
)

# Combine all parts
result = body.union(plate).union(plug)