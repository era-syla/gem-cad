import cadquery as cq

# Base disk
base = cq.Workplane("XY").circle(50).extrude(8)

# Add two hollow cylindrical posts on top of the base
# Post 1: offset from center
post1_outer = (
    cq.Workplane("XY")
    .transformed(offset=(20, -15, 0))
    .circle(6)
    .extrude(20)
)

post1_inner = (
    cq.Workplane("XY")
    .transformed(offset=(20, -15, 0))
    .circle(3)
    .extrude(28)
)

# Post 2: offset from center on other side
post2_outer = (
    cq.Workplane("XY")
    .transformed(offset=(-10, 20, 0))
    .circle(6)
    .extrude(28)
)

post2_inner = (
    cq.Workplane("XY")
    .transformed(offset=(-10, 20, 0))
    .circle(3)
    .extrude(36)
)

# Combine base with posts
result = (
    base
    .union(post1_outer)
    .cut(post1_inner)
    .union(post2_outer)
    .cut(post2_inner)
)