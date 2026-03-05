import cadquery as cq

# Build a hose clamp / ring clamp assembly
# Main ring (large circular band)
ring_outer_r = 45
ring_inner_r = 43
ring_height = 3

# Create the main ring
ring = (
    cq.Workplane("XY")
    .circle(ring_outer_r)
    .circle(ring_inner_r)
    .extrude(ring_height)
)

# Base plate for the clamp mechanism
base = (
    cq.Workplane("XY")
    .box(22, 18, 4)
    .translate((0, ring_outer_r - 5, ring_height / 2))
)

# Combine ring and base
result = ring.union(base)

# Lower mounting plate (wider, flatter)
mount_plate = (
    cq.Workplane("XY")
    .box(26, 22, 2)
    .translate((0, ring_outer_r - 5, ring_height + 4 - 1))
)
result = result.union(mount_plate)

# Clamp body (main block)
clamp_body = (
    cq.Workplane("XY")
    .box(18, 14, 10)
    .translate((0, ring_outer_r - 4, ring_height + 4 + 5))
)
result = result.union(clamp_body)

# Jaw front
jaw_front = (
    cq.Workplane("XY")
    .box(18, 3, 8)
    .translate((0, ring_outer_r - 4 + 8.5, ring_height + 4 + 6))
)
result = result.union(jaw_front)

# Jaw back
jaw_back = (
    cq.Workplane("XY")
    .box(18, 3, 8)
    .translate((0, ring_outer_r - 4 - 8.5, ring_height + 4 + 6))
)
result = result.union(jaw_back)

# Screw rod (horizontal adjustment screw)
screw_rod = (
    cq.Workplane("YZ")
    .circle(1.5)
    .extrude(22)
    .translate((-11, ring_outer_r - 4, ring_height + 4 + 10))
)
result = result.union(screw_rod)

# Screw head knob
screw_head = (
    cq.Workplane("XY")
    .cylinder(3, 4)
    .translate((12, ring_outer_r - 4, ring_height + 4 + 10))
)
result = result.union(screw_head)

# Left post
left_post = (
    cq.Workplane("XY")
    .cylinder(6, 2)
    .translate((-7, ring_outer_r - 4, ring_height + 4 + 3))
)
result = result.union(left_post)

# Right post
right_post = (
    cq.Workplane("XY")
    .cylinder(6, 2)
    .translate((7, ring_outer_r - 4, ring_height + 4 + 3))
)
result = result.union(right_post)

# Small cylinder details on top of clamp body
top_cyl1 = (
    cq.Workplane("XY")
    .cylinder(4, 2.5)
    .translate((-4, ring_outer_r - 4, ring_height + 4 + 14))
)
result = result.union(top_cyl1)

top_cyl2 = (
    cq.Workplane("XY")
    .cylinder(4, 2.5)
    .translate((4, ring_outer_r - 4, ring_height + 4 + 14))
)
result = result.union(top_cyl2)