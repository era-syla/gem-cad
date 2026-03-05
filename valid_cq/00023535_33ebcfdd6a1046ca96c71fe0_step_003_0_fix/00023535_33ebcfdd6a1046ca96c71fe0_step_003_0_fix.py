import cadquery as cq

# Base with U-shaped channel
base = (
    cq.Workplane("XY")
    .box(200, 80, 40)
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .rect(180, 60)
    .cutThruAll()
)

# Fixed jaw at back
fixed = (
    cq.Workplane("XY")
    .transformed(offset=(80, 0, 20))
    .box(40, 80, 40)
)

# Sliding jaw at front with screw hole
slide = (
    cq.Workplane("XY")
    .transformed(offset=(-85, 0, 20))
    .box(30, 80, 40)
    .faces(">X")
    .workplane()
    .circle(7)
    .cutBlind(-40)
)

# Main screw (smooth cylinder)
screw = (
    cq.Workplane("YZ")
    .transformed(offset=(-85, 0, 22))
    .circle(6)
    .extrude(165)
)

# T-handle rod
rod = (
    cq.Workplane("XZ")
    .circle(2)
    .extrude(60)
    .translate((-85, 0, 22))
)

# Handle knobs
knob1 = (
    cq.Workplane("YZ")
    .circle(4)
    .extrude(3)
    .translate((-85, 30, 22))
)
knob2 = knob1.translate((0, -60, 0))

# Combine all parts into final result
result = base.union(fixed).union(slide).union(screw).union(rod).union(knob1).union(knob2)