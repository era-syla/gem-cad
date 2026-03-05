import cadquery as cq

result = (
    cq.Workplane("XY")
    .cylinder(8, 25)
    .faces(">Z").workplane()
    .polarArray(20, 0, 360, 3)
    .rect(30, 8)
    .extrude(20)
    .faces(">Z").workplane()
    .circle(5)
    .extrude(15)
)