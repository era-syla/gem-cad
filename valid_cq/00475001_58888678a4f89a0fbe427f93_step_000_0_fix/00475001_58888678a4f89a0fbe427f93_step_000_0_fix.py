import cadquery as cq

body = (
    cq.Workplane("YZ")
    .circle(6)
    .transformed(offset=(20,0,0))
    .circle(4)
    .transformed(offset=(60,0,0))
    .circle(2)
    .loft()
)

boom1 = (
    cq.Workplane("YZ")
    .transformed(offset=(0,-8,-2))
    .circle(1.5)
    .extrude(100)
)

boom2 = (
    cq.Workplane("YZ")
    .transformed(offset=(0,8,-2))
    .circle(1.5)
    .extrude(100)
)

fin = (
    cq.Workplane("XZ")
    .transformed(offset=(60,0,-4))
    .polyline([(0,0),(0,10),(20,0)])
    .close()
    .extrude(1)
)

intake = (
    cq.Workplane("YZ")
    .transformed(offset=(100,0,2))
    .box(4,8,4)
)

result = body.union(boom1).union(boom2).union(fin).union(intake)