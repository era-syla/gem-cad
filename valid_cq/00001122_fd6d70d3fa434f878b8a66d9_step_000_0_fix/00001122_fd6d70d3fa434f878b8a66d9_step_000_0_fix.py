import cadquery as cq

# Base plate
base = (
    cq.Workplane("XY")
    .rect(100, 60)
    .extrude(10)
    .edges("|Z")
    .fillet(5)
)

# Fixed jaw
jaw1 = (
    cq.Workplane("XY")
    .box(20, 40, 15)
    .translate((-15, 0, 10))
)

# Moving jaw
jaw2 = (
    cq.Workplane("XY")
    .box(20, 40, 15)
    .translate((15, 0, 10))
)

# Screw rod
screw = (
    cq.Workplane("XY")
    .circle(3)
    .extrude(60)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((0, -20, 17.5))
)

# Handle
handle = (
    cq.Workplane("XY")
    .circle(2)
    .extrude(80)
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((0, -25, 17.5))
)

# Loop path for sweep
path = cq.Workplane("XY").circle(70).wires().val()

# Thin loop swept along the circle
loop = (
    cq.Workplane("XY")
    .circle(1)
    .sweep(path)
    .rotate((0, 0, 0), (1, 0, 0), 90)
    .translate((0, 50, 30))
)

result = base.union(jaw1).union(jaw2).union(screw).union(handle).union(loop)