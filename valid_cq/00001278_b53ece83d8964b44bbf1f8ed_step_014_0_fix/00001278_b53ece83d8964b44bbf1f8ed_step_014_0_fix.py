import cadquery as cq

# Base of the container
base = (
    cq.Workplane("XY")
    .rect(100, 70)
    .extrude(25)
    .edges("|Z")
    .fillet(15)
)

# Lid of the container
lid = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 25))
    .rect(94, 64)
    .extrude(23)
    .edges("|Z")
    .fillet(13)
)

# Top recess in the lid
recess = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 25 + 23))
    .rect(70, 50)
    .extrude(-5)
)

# Combine base and lid, then cut the recess
result = base.union(lid).cut(recess)