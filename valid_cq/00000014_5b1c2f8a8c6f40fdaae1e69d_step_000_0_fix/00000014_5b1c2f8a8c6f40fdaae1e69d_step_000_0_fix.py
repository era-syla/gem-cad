import cadquery as cq

# Build a mechanical pencil along the X axis

# Main body - hexagonal barrel
barrel = (
    cq.Workplane("YZ")
    .polygon(6, 11)
    .extrude(80)
)

# Translate barrel to start at x=20
barrel = barrel.translate((20, 0, 0))

# Rear cap - cylinder at back end
rear_cap = (
    cq.Workplane("YZ")
    .circle(5.5)
    .extrude(20)
)

# Front grip section - cylinder
front_grip = (
    cq.Workplane("YZ")
    .circle(5)
    .extrude(20)
    .translate((100, 0, 0))
)

# Front taper section
front_taper = (
    cq.Workplane("YZ")
    .circle(5)
    .workplane(offset=25)
    .circle(2.5)
    .loft()
    .translate((120, 0, 0))
)

# Tip section
tip1 = (
    cq.Workplane("YZ")
    .circle(2.5)
    .workplane(offset=15)
    .circle(1.5)
    .loft()
    .translate((145, 0, 0))
)

tip2 = (
    cq.Workplane("YZ")
    .circle(1.5)
    .workplane(offset=10)
    .circle(0.8)
    .loft()
    .translate((160, 0, 0))
)

# Very tip - thin needle
needle = (
    cq.Workplane("YZ")
    .circle(0.8)
    .workplane(offset=8)
    .circle(0.15)
    .loft()
    .translate((170, 0, 0))
)

# Clip on top of barrel
clip_base = (
    cq.Workplane("XY")
    .transformed(offset=(60, 5.5, 0))
    .rect(30, 3)
    .extrude(3)
)

clip_end = (
    cq.Workplane("XY")
    .transformed(offset=(75, 5.5, 0))
    .rect(4, 4)
    .extrude(5)
)

# Combine all parts
result = (
    barrel
    .union(rear_cap)
    .union(front_grip)
    .union(front_taper)
    .union(tip1)
    .union(tip2)
    .union(needle)
    .union(clip_base)
    .union(clip_end)
)

# Add some grooves to the grip section - rings
for i in range(4):
    groove = (
        cq.Workplane("YZ")
        .circle(5.2)
        .workplane(offset=2)
        .circle(4.5)
        .loft()
        .translate((102 + i * 4, 0, 0))
    )
    result = result.cut(
        cq.Workplane("YZ")
        .circle(5.3)
        .extrude(1.5)
        .translate((103 + i * 4, 0, 0))
    )

# Rotate the whole thing to match the image diagonal orientation
result = result.rotate((0, 0, 0), (0, 0, 1), 35)