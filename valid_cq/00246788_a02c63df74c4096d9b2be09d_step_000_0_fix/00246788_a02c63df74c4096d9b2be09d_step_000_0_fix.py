import cadquery as cq
import math

# Parameters
p1 = (0, 0)
p2 = (80, 0)
p3 = (40, 60)
r = 20
thickness = 10

def rect_between(a, b, radius, thickness):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    angle = math.degrees(math.atan2(dy, dx))
    midx, midy = (ax + bx) / 2, (ay + by) / 2
    return (
        cq.Workplane('XY')
        .transformed(offset=(midx, midy, 0), rotate=(0, 0, angle))
        .rect(length - 2 * radius, 2 * radius)
        .extrude(thickness)
    )

# Create corner circles
c1 = cq.Workplane('XY').center(*p1).circle(r).extrude(thickness)
c2 = cq.Workplane('XY').center(*p2).circle(r).extrude(thickness)
c3 = cq.Workplane('XY').center(*p3).circle(r).extrude(thickness)

# Create side connectors
s12 = rect_between(p1, p2, r, thickness)
s23 = rect_between(p2, p3, r, thickness)
s31 = rect_between(p3, p1, r, thickness)

# Union all parts
result = c1.union(c2).union(c3).union(s12).union(s23).union(s31)