import cadquery as cq

# Base plate
result = cq.Workplane("XY").box(100, 20, 5)

# Vertical post
post = cq.Workplane("XY").workplane(offset=5).center(-35, 0).circle(5).extrude(15)
result = result.union(post)

# Small holes and mounts
result = result.faces(">Z").workplane().center(-30, 0).hole(6)
result = result.faces(">Z").workplane().center(0, 0).hole(3)

# Elongated blocks on the base plate
block1 = cq.Workplane("XY").workplane(offset=5).center(25, 0).box(10, 5, 5)
block2 = block1.mirror("YZ").translate((0, 10, 0))
result = result.union(block1).union(block2)