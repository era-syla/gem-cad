import cadquery as cq

result = cq.Workplane("XZ").polyline([
    (0, 0),
    (0, 5),
    (20, 5),
    (30, 15),
    (80, 15),
    (100, 10),
    (100, 0)
]).close().extrude(10)

result = result.faces("<Z").workplane().center(90, 0).circle(3).extrude(5)