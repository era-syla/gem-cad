import cadquery as cq
import math

# Parameters
inner_d = 25.0
outer_d = 47.0
width = 14.0
ball_d = 7.0
ball_count = 8

inner_r = inner_d / 2.0
outer_r = outer_d / 2.0
ball_r = ball_d / 2.0
ball_center_r = (inner_r + outer_r) / 2.0
half_w = width / 2.0

# Create outer and inner ring
result = (
    cq.Workplane("XY")
    .circle(outer_r)
    .circle(inner_r)
    .extrude(width)
    .edges()
    .fillet(1.0)
)

# Add the balls
for i in range(ball_count):
    angle = 360.0 / ball_count * i
    rad = math.radians(angle)
    x = ball_center_r * math.cos(rad)
    y = ball_center_r * math.sin(rad)
    ball = cq.Workplane("XY").transformed(offset=(x, y, half_w)).sphere(ball_r)
    result = result.union(ball)