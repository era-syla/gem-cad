import cadquery as cq
import math

# Ball bearing parameters
outer_radius = 30
inner_radius = 12
ball_radius = 6
bearing_height = 14
race_depth = 2

# Outer ring
outer_ring = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(outer_radius - 6)
    .extrude(bearing_height)
)

# Inner ring
inner_ring = (
    cq.Workplane("XY")
    .circle(inner_radius + 6)
    .circle(inner_radius)
    .extrude(bearing_height)
)

# Ball center radius
ball_center_r = (outer_radius - 6 + inner_radius + 6) / 2

# Balls
num_balls = 8
balls = None
for i in range(num_balls):
    angle = 2 * math.pi * i / num_balls
    x = ball_center_r * math.cos(angle)
    y = ball_center_r * math.sin(angle)
    ball = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(x, y, bearing_height / 2))
        .sphere(ball_radius)
    )
    if balls is None:
        balls = ball
    else:
        balls = balls.union(ball)

# Combine outer and inner rings
result = outer_ring.union(inner_ring)

# Cut groove in outer ring (inner surface groove)
outer_groove = (
    cq.Workplane("XY")
    .workplane(offset=bearing_height / 2)
    .circle(outer_radius - 6 + ball_radius * 0.3)
    .circle(outer_radius - 6 - ball_radius * 0.3)
    .extrude(ball_radius * 0.6)
    .translate((0, 0, -ball_radius * 0.3))
)

# Cut groove in inner ring (outer surface groove)
inner_groove = (
    cq.Workplane("XY")
    .workplane(offset=bearing_height / 2)
    .circle(inner_radius + 6 + ball_radius * 0.3)
    .circle(inner_radius + 6 - ball_radius * 0.3)
    .extrude(ball_radius * 0.6)
    .translate((0, 0, -ball_radius * 0.3))
)

# Add balls to result
if balls is not None:
    result = result.union(balls)

# Cage / retainer ring - a thin ring between inner and outer
cage_r_mid = ball_center_r
cage_thickness = 1.5
cage_height = bearing_height * 0.6
cage_z = (bearing_height - cage_height) / 2

cage = (
    cq.Workplane("XY")
    .workplane(offset=cage_z)
    .circle(cage_r_mid + cage_thickness)
    .circle(cage_r_mid - cage_thickness)
    .extrude(cage_height)
)

# Cut holes in cage for balls
cage_with_holes = cage
for i in range(num_balls):
    angle = 2 * math.pi * i / num_balls
    x = ball_center_r * math.cos(angle)
    y = ball_center_r * math.sin(angle)
    hole = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(x, y, bearing_height / 2))
        .sphere(ball_radius * 1.05)
    )
    cage_with_holes = cage_with_holes.cut(hole)

result = result.union(cage_with_holes)