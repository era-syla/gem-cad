import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(40, 6, 3)
    .edges("|Z").fillet(1)
    .faces(">Z").workplane(centerOption="CenterOfMass")
    .circle(6).extrude(3).faces(">Z").workplane(centerOption="CenterOfMass")
    .circle(3).cutThruAll()
    .faces(">Z").workplane(offset=-3).center(0, 19)
    .circle(3).extrude(6)
    .faces(">Z").workplane().hole(2)
    .faces("<Z").workplane(centerOption="CenterOfMass")
    .rarray(10, 1, 2, 1).circle(2).cutThruAll()
)