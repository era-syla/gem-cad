import cadquery as cq

# Create the tapered base as a rectangular frustum
base = (
    cq.Workplane("XY")
    .rect(40, 30)
    .workplane(offset=80)
    .rect(25, 15)
    .loft()
)

# Create the vertical post on top of the frustum
post = (
    cq.Workplane("XY")
    .workplane(offset=80)
    .rect(25, 15)
    .extrude(40)
)

# Combine base and post
result = base.union(post)

# Cut the U-shaped channel into the top of the post
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(15, 15)
    .cutBlind(-10)
)