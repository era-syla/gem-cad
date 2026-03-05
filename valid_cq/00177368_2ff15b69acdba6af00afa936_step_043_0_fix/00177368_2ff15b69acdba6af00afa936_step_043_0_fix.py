import cadquery as cq
import math

length, width, thickness = 80, 10, 5
hole_r = 3

# Create three arms as boxes and union them
angles = [0, 120, 240]
result = None
for angle in angles:
    arm = (cq.Workplane("XY")
           .box(length, width, thickness)
           .translate((length/2, 0, thickness/2))
           .rotate((0, 0, 0), (0, 0, 1), angle))
    result = arm if result is None else result.union(arm)

# Fillet all edges
result = result.edges().fillet(2)

# Cut holes at each arm end and at center
hole_height = thickness + 10
for angle in angles + [None]:
    if angle is None:
        x, y = 0, 0
    else:
        x = length * math.cos(math.radians(angle))
        y = length * math.sin(math.radians(angle))
    cyl = (cq.Workplane("XY")
           .transformed(offset=(x, y, -hole_height/2))
           .circle(hole_r)
           .extrude(hole_height))
    result = result.cut(cyl)

# Create ball joints at each hole location
ball_positions = [(length * math.cos(math.radians(a)), length * math.sin(math.radians(a)), thickness) 
                  for a in angles] + [(0, 0, thickness)]
balls = None
for x, y, z in ball_positions:
    base = (cq.Workplane("XY")
            .transformed(offset=(x, y, z))
            .circle(4)
            .extrude(4))
    sphere = (cq.Workplane("XY")
              .transformed(offset=(x, y, z + 4))
              .sphere(6))
    ball = base.union(sphere)
    balls = ball if balls is None else balls.union(ball)

result = result.union(balls)