import cadquery as cq

# Base plate
result = cq.Workplane("XY").rect(100, 300).extrude(5)

# Top hooks
hook_length = 30
hook_width = 3
for x, y, ang in [(-30, 260, -15), (0, 240, 0), (30, 220, 15)]:
    hook = (
        cq.Workplane("XY")
        .workplane(offset=5)
        .center(x, y)
        .rect(hook_length, hook_width)
        .extrude(5)
        .rotate((x, y, 5), (x, y, 6), ang)
    )
    result = result.union(hook)

# Middle bracket
points = [(-20, 140), (20, 140), (40, 110), (20, 80), (-20, 80), (-40, 110)]
bracket = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .polyline(points)
    .close()
    .extrude(5)
)
result = result.union(bracket)

# Right side support
support = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .center(40, 80)
    .rect(40, 80)
    .extrude(5)
    .rotate((40, 80, 5), (40, 80, 6), -30)
)
result = result.union(support)