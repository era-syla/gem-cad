import cadquery as cq

# Axle
axle = cq.Workplane("XY").circle(5).extrude(200).translate((0, 0, -100))

# Hub shell (frustum)
hub_shell = (
    cq.Workplane("XY")
    .circle(20)
    .workplane(offset=120)
    .circle(30)
    .loft()
    .translate((0, 0, -60))
)

# Left flange with 6 bolt holes
left_flange = (
    cq.Workplane("XY")
    .workplane(offset=-60)
    .circle(20)
    .extrude(5)
    .faces(">Z")
    .workplane()
    .polarArray(15, 0, 360, 6)
    .hole(4)
)

# Right flange with 24 spoke holes
right_flange = (
    cq.Workplane("XY")
    .workplane(offset=60)
    .circle(28)
    .extrude(5)
    .faces(">Z")
    .workplane()
    .polarArray(20, 0, 360, 24)
    .hole(3)
)

# Freehub body
freehub = (
    cq.Workplane("XY")
    .workplane(offset=65)
    .circle(15)
    .extrude(40)
)

# Assemble all parts
result = axle.union(hub_shell).union(left_flange).union(right_flange).union(freehub)