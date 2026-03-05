import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(50, 20, 10)
    .edges("|Z")
    .fillet(2)
    .faces(">Z")
    .workplane()
    .hole(10, 5)
    .faces(">Z")
    .workplane(offset=-5)
    .hole(15, 5)
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .rarray(25, 10, 2, 1)
    .hole(5)
)