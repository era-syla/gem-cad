import cadquery as cq

result = (
    cq.Workplane("front")
    .moveTo(0, 0)
    .lineTo(10, 0)
    .lineTo(20, 30)
    .lineTo(10, 100)
    .lineTo(0, 110)
    .lineTo(-10, 100)
    .lineTo(-20, 30)
    .close()
    .extrude(5)
    .faces("<Z")
    .workplane()
    .pushPoints([(0, 10), (0, 50), (-10, 100), (10, 100)])
    .hole(5)
)