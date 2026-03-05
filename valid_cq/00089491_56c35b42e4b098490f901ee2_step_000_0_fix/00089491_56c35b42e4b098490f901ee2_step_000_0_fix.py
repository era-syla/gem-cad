import cadquery as cq

# Create the base
base = cq.Workplane("XY").rect(60, 20).extrude(5)

# Create cutouts in the base
cutouts = (
    base.faces(">Z")
    .workplane()
    .rarray(15, 15, 4, 1)
    .rect(5, 15)
    .cutThruAll()
)

# Create the main body
body = (
    cutouts.faces(">Z")
    .workplane(offset=5)
    .rect(30, 20)
    .extrude(20)
)

# Create the circular feature with spokes
spokeBase = (
    body.faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(10)
    .extrude(5)
)

# Add spokes
spokes = spokeBase.faces(">Z").workplane().rarray(5, 5, 8, 1).circle(1).cutBlind(-5)

# Create the U-shaped feature
uShape = (
    body.faces(">Z")
    .workplane(offset=5)
    .center(0, 0)
    .rect(10, 20)
    .extrude(15)
    .edges("|Z")
    .fillet(1)
)

# Create the cylindrical rod
rod = (
    body.faces(">Z")
    .workplane(offset=15)
    .center(0, 0)
    .circle(2)
    .extrude(30)
)

# Combine all parts
result = base.union(spokeBase).union(uShape).union(rod)