import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(70, 40)
    .extrude(5)
    .edges("|Z")
    .fillet(5)
    .faces(">Z")
    .workplane(invert=True)
    .rarray(30, 20, 2, 2)
    .circle(3)
    .cutThruAll()
)