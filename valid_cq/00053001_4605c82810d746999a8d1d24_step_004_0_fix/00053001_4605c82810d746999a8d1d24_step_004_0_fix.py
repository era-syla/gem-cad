import cadquery as cq

# Base block
block = cq.Workplane("XY").box(200, 40, 10)

# Pocket cuts: two elongated elliptical pockets on top
cut1 = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .center(-50, 0)
    .ellipse(60, 15)
    .extrude(-6)
)
cut2 = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .center(50, 0)
    .ellipse(60, 15)
    .extrude(-4)
)

# Apply cuts and add mounting holes
result = (
    block
    .cut(cut1)
    .cut(cut2)
    .faces("<X")
    .workplane(centerOption="CenterOfBoundBox")
    .center(0, 15).circle(2).cutThruAll()
    .center(0, -30).circle(2).cutThruAll()
)