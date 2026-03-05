import cadquery as cq

thickness = 3

result = (
    cq.Workplane("XY")
    .polyline([
        (-60, 40),
        (60, 40),
        (60, -20),
        (40, -40),
        (20, -40),
        (20, -20),
        (-20, -20),
        (-20, -40),
        (-40, -40),
        (-60, -20),
    ])
    .close()
    .extrude(thickness)
    # small mounting holes
    .faces(">Z")
    .workplane()
    .pushPoints([(-50, 30), (50, 30), (-50, -10), (50, -10), (0, -10)])
    .hole(5)
    # left medium hole
    .faces(">Z")
    .workplane()
    .pushPoints([(-10, 10)])
    .hole(10)
    # right medium hole
    .faces(">Z")
    .workplane()
    .pushPoints([(10, 10)])
    .hole(15)
)