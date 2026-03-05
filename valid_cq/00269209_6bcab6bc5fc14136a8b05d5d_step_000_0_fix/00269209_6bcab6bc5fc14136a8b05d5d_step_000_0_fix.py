import cadquery as cq

# Base cylinder
cyl = cq.Workplane("XY").circle(10).extrude(50)

# Hex shaft at one end
hex_shaft = (
    cq.Workplane("XY")
    .workplane(offset=50)
    .polygon(6, 8)
    .extrude(15)
)

# Combine cylinder and shaft
body = cyl.union(hex_shaft)

# Cut four rectangular windows
for angle in (0, 90, 180, 270):
    cut_box = (
        cq.Workplane("XY")
        .box(6, 40, 30)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .translate((7, 0, 25))
    )
    body = body.cut(cut_box)

result = body