import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(80, 40, 5)
    # Slot cut: rectangle plus two end circles
    .faces(">Z").workplane()
    .center(-20, 0).rect(30, 10).cutThruAll()
    .faces(">Z").workplane()
    .pushPoints([(-35, 0), (-5, 0)]).circle(5).cutThruAll()
    # Four hole pattern on right side
    .faces(">Z").workplane()
    .pushPoints([(30, 0), (10, 0), (20, 10), (20, -10)]).circle(4).cutThruAll()
)