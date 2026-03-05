import cadquery as cq

# Base plate
base = cq.Workplane("XY").rect(60, 10).extrude(5)

# Upright plate
upright = (
    cq.Workplane("XY")
    .center(0, 5)
    .rect(60, 50)
    .extrude(2)
    .edges("|Z")
    .fillet(1)
)

# Cutout in the upright plate
cutout = (
    cq.Workplane("XY")
    .center(0, 5)
    .moveTo(0, -30)
    .rect(20, 10)
    .extrude(2)
)

# Combine and cut
result = upright.cut(cutout).union(base)

# Holes in the base plate
result = result.faces(">Z").workplane().pushPoints([(-25, 0), (25, 0)]).hole(3)

# Holes in the upright plate
result = result.faces(">Y").workplane().pushPoints([(-25, 0), (25, 0)]).hole(3)