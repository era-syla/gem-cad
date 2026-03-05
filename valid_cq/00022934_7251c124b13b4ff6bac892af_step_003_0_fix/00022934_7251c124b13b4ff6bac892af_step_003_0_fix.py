import cadquery as cq

# Base with side walls
base = (
    cq.Workplane("XY")
    .box(200, 80, 20)
    .faces(">Z")
    .shell(-10)
)

# Fixed and movable supports (jaw blocks)
support1 = (
    cq.Workplane("XY")
    .workplane(offset=20)
    .transformed(offset=(-80, 0, 0))
    .box(20, 60, 30)
    .faces(">X")
    .workplane()
    .hole(10)
)
support2 = (
    cq.Workplane("XY")
    .workplane(offset=20)
    .transformed(offset=(80, 0, 0))
    .box(20, 60, 30)
    .faces("<X")
    .workplane()
    .hole(10)
)

# Screw (smooth cylinder)
screw = (
    cq.Workplane("YZ", origin=(-80, 0, 35))
    .circle(4)
    .extrude(160)
)

# T-handle on screw end
handle = (
    cq.Workplane("XZ", origin=(80, 0, 35))
    .circle(2)
    .extrude(60)
    .faces(">Y")
    .workplane()
    .circle(3)
    .extrude(2)
    .faces("<Y")
    .workplane()
    .circle(3)
    .extrude(2)
)

# Assemble all parts
result = base.union(support1).union(support2).union(screw).union(handle)