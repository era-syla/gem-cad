import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(50, 20)
    .extrude(20)
    .edges("|Z and >X")
    .fillet(5)
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .hole(5)
)