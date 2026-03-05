import cadquery as cq
import math

# Main body
body = (
    cq.Workplane("XY")
    .box(50, 30, 25, centered=(True, True, False))
    .edges("|Z")
    .fillet(1)
)

# Top tube
top_tube = (
    cq.Workplane("XY")
    .workplane(offset=25)
    .circle(10)
    .extrude(10)
    .faces(">Z")
    .circle(8)
    .cutBlind(10)
)

# Front cylinder
front_cyl = (
    cq.Workplane("YZ")
    .workplane(offset=25)
    .circle(7.5)
    .extrude(15)
)

# Lever arm (flat L-shaped bracket)
lever = (
    cq.Workplane("XY")
    .workplane(offset=12.5)
    .transformed(offset=(-25, 0, 0))
    .polyline([(0, 0), (20, 0), (20, 5), (5, 5), (5, 30), (0, 30)])
    .close()
    .extrude(3)
    .edges("|Z")
    .fillet(1)
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .hole(5)
)

# Knob cylinder on right side
knob = (
    cq.Workplane("YZ")
    .workplane(offset=25)
    .transformed(offset=(0, 0, 12.5))
    .circle(5)
    .extrude(15)
)

# Knurled ridges around the knob
knurl_pts = [
    (5 * math.cos(math.radians(a)), 5 * math.sin(math.radians(a)))
    for a in range(0, 360, 30)
]
knurled_ridges = (
    cq.Workplane("YZ")
    .workplane(offset=25)
    .transformed(offset=(0, 0, 12.5))
    .pushPoints(knurl_pts)
    .circle(1)
    .extrude(15)
)

result = (
    body
    .union(top_tube)
    .union(front_cyl)
    .union(lever)
    .union(knob)
    .union(knurled_ridges)
)