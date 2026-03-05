import cadquery as cq

thickness = 5
outline = [
    (0, 0),
    (60, 0),
    (60, 10),
    (55, 70),
    (40, 90),
    (30, 140),
    (0, 140),
]

result = (
    cq.Workplane("XY")
    .polyline(outline)
    .close()
    .extrude(thickness)
    .edges("|Z").fillet(3)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (10, 3),
        (50, 13),
        (52, 72),
        (35, 92),
        (25, 137),
    ])
    .hole(8)
)