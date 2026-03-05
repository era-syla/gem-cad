import cadquery as cq

# Base
base = cq.Workplane("XY").rect(80, 60).extrude(5).edges("|Z").fillet(5)

# Pivot cylinder
pivot = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .circle(10)
    .extrude(10)
)

# Support arm
arm = (
    cq.Workplane("XY")
    .workplane(offset=15)
    .circle(2)
    .extrude(20)
)

# Fixed jaw
fixed = (
    cq.Workplane("XY")
    .workplane(offset=35)
    .box(20, 5, 10)
    .translate((0, 0, 5))
    .edges("|Z")
    .fillet(1)
)

# Sliding jaw
sliding = (
    cq.Workplane("XY")
    .workplane(offset=35)
    .box(20, 5, 10)
    .translate((15, 0, 5))
    .edges("|Z")
    .fillet(1)
)

# Screw
screw = (
    cq.Workplane("XY")
    .workplane(offset=40)
    .circle(1)
    .extrude(15)
)

# Decorative ring
ring = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .circle(30)
    .circle(25)
    .extrude(2)
)

result = base.union(pivot).union(arm).union(fixed).union(sliding).union(screw).union(ring)