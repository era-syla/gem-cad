import cadquery as cq

result = (
    cq.Workplane("XY")
    .moveTo(-20, 0).lineTo(-10, 10).lineTo(-5, 10).lineTo(0, 5)
    .lineTo(5, 10).lineTo(10, 10).lineTo(20, 0)
    .lineTo(10, -10).lineTo(-10, -10).close()
    .extrude(3)
    .faces(">Z").workplane()
    .hole(15, 2)
    .hole(5, 0.5).rect(2, 2, forConstruction=True)
    .vertices().cboreHole(1.5, 3, 2)
)