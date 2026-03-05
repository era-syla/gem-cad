import cadquery as cq

thickness = 8

points = [
    (0, 0),
    (80, 0),
    (90, 10),
    (50, 60),
    (50, 120),
    (0, 120)
]

result = cq.Workplane("XZ").polyline(points).close().extrude(thickness)

# Drill holes through thickness on the long angled segment
hole_positions = [(85, 5), (75, 25), (65, 45)]
result = result.faces(">Y").workplane().pushPoints(hole_positions).hole(5)

# Drill a hole in the vertical riser
result = result.faces(">Y").workplane().pushPoints([(10, 100)]).hole(5)

# Drill a hole in the foot section
result = result.faces(">Y").workplane().pushPoints([(20, 5)]).hole(5)

# Cut a slot at the foot end face
result = result.faces(">X").workplane().center(0, 5).rect(thickness, 10).cutThruAll()

result