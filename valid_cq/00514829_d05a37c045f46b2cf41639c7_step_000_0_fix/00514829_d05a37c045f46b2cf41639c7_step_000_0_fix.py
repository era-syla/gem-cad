import cadquery as cq

# Base profile
base = (
    cq.Workplane("XY")
    .polyline([(20, 0), (10, 15), (-10, 12), (-20, 0), (-10, -12), (10, -15)])
    .close()
    .extrude(5)
    .edges("|Z").fillet(2)
)

# Add cylinders and ramp
result = (
    base
    .union(
        cq.Workplane("XY")
        .workplane(offset=5)
        .center(0, 0)
        .circle(6)
        .extrude(20)
    )
    .union(
        cq.Workplane("XY")
        .workplane(offset=5)
        .center(-10, 8)
        .circle(5)
        .extrude(15)
    )
    .union(
        cq.Workplane("XY")
        .workplane(offset=5)
        .center(12, 3)
        .circle(4)
        .extrude(10)
    )
    .union(
        cq.Workplane("XY")
        .workplane(offset=5)
        .center(5, -10)
        .circle(3)
        .extrude(18)
    )
    .union(
        cq.Workplane("XY")
        .workplane(offset=5)
        .center(18, 0)
        .polyline([(0, 0), (10, 0), (0, 10)])
        .close()
        .extrude(15)
    )
)