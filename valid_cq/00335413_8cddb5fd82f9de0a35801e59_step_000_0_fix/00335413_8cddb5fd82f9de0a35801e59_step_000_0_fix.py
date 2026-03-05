import cadquery as cq

outline = [
    (0, 0), (20, 0), (25, 5), (20, 10),
    (10, 10), (5, 5), (0, 10)
]

star_points = [
    (5, 0), (7, -3), (10, 0), (8, -5),
    (10, -10), (5, -7), (0, -10), (2, -5)
]

outline_wire = cq.Workplane("XY").polyline(outline).close()
star_wire = cq.Workplane("XY").polyline(star_points).close()

outline_extrude = outline_wire.extrude(2)
star_extrude = star_wire.extrude(2)

result = outline_extrude.union(star_extrude)