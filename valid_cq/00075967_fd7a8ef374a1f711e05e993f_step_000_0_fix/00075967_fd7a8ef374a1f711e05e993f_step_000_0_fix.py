import cadquery as cq

# Base block
base = cq.Workplane("XY").box(60, 60, 10)

# Cylindrical boss
cyl_h = 12
boss = cq.Workplane("XY").circle(10).extrude(cyl_h).translate((0, 27, 10))

# Arch cut
arch = (
    cq.Workplane("XZ")
    .moveTo(0, 10)
    .threePointArc((10, 20), (30, 20))
    .lineTo(30, 0)
    .close()
    .extrude(10, both=True)
    .translate((0, 0, 10))
)

# Combine all parts
result = base.union(boss).cut(arch)