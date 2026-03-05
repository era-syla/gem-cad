import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(30, 10, 10)
    .faces(">Y")
    .workplane(offset=0)
    .circle(10)
    .extrude(20)
    .faces(">Z")
    .workplane(centerOption='CenterOfBoundBox')
    .circle(5)
    .cutThruAll()
)