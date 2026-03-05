import cadquery as cq

# Base cylinder
base = cq.Workplane("XY") \
    .circle(10) \
    .extrude(20)

# Ball for joint
ball = cq.Workplane("XY") \
    .transformed(offset=(0, 0, 20)) \
    .sphere(8)

# Ring around the joint (socket housing)
ring_outer = cq.Workplane("XY") \
    .transformed(offset=(0, 0, 20)) \
    .circle(12) \
    .extrude(3)
ring_inner = cq.Workplane("XY") \
    .transformed(offset=(0, 0, 20)) \
    .circle(8) \
    .extrude(3)
ring = ring_outer.cut(ring_inner)

# Rod attached to the ball joint
rod = cq.Workplane("YZ") \
    .transformed(offset=(8, 0, 20)) \
    .circle(2) \
    .extrude(200)

# Combine all parts
result = base.union(ball).union(ring).union(rod)