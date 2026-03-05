import cadquery as cq
import math

thickness = 5

# Part 1: L-shaped bracket with small holes
leg_long = 80
leg_short = 50
notch = 10
hole_dia = 6

pts1 = [(0, 0), (leg_long, 0), (leg_long, leg_short), (notch, leg_short), (0, notch)]
part1 = (
    cq.Workplane("XY")
    .polyline(pts1)
    .close()
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .pushPoints(
        [
            (10 + i * ((leg_long - 2 * 10) / (4 - 1)), 10)
            for i in range(4)
        ]
        + [
            (leg_long - 10, 10 + j * ((leg_short - 2 * 10) / (3 - 1)))
            for j in range(3)
        ]
    )
    .hole(hole_dia)
)

# Part 2: Triangular bracket with a large center hole and small around
width = 80
height = 60
big_hole_dia = 30
small_hole_dia = 6
ring_radius = 20
cx = width / 2
cy = height / 2

pts2 = [(0, height), (width, height), (cx, 0)]
part2 = (
    cq.Workplane("XY")
    .polyline(pts2)
    .close()
    .extrude(thickness)
    .faces(">Z")
    .workplane()
    .center(cx, cy)
    .hole(big_hole_dia)
    .pushPoints(
        [
            (
                ring_radius * math.cos(math.radians(a)),
                ring_radius * math.sin(math.radians(a)),
            )
            for a in range(0, 360, 60)
        ]
    )
    .hole(small_hole_dia)
    .workplane()
    .center(cx - width + 10, cy - height + 10)
    .pushPoints([(-cx + 10, height - 10 - cy), (cx - 10, height - 10 - cy)])
    .hole(small_hole_dia)
)

# Position part2 relative to part1
part2 = part2.translate((100, 50, 0))

result = part1.union(part2)