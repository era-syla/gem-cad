import cadquery as cq

# Base box
base = cq.Workplane("XY").box(10, 10, 1)

# First platform with post
platform1 = (
    cq.Workplane("XY")
    .workplane(offset=3)
    .box(8, 8, 1)
    .workplane(centerOption='CenterOfBoundBox')
    .circle(1).extrude(3)
)

# Connecting cylinders
connect1 = (
    cq.Workplane("XY")
    .workplane(offset=4.5)
    .polarArray(4, 0, 360, 6)
    .circle(0.2).extrude(5)
)

platform2 = (
    cq.Workplane("XY")
    .workplane(offset=10)
    .box(6, 6, 1)
    .workplane(centerOption='CenterOfBoundBox')
    .circle(1).extrude(3)
)

connect2 = (
    cq.Workplane("XY")
    .workplane(offset=11.5)
    .polarArray(3, 0, 360, 6)
    .circle(0.2).extrude(5)
)

platform3 = (
    cq.Workplane("XY")
    .workplane(offset=17)
    .box(4, 4, 1)
    .workplane(centerOption='CenterOfBoundBox')
    .circle(1).extrude(3)
)

result = base.union(platform1).union(connect1).union(platform2).union(connect2).union(platform3)