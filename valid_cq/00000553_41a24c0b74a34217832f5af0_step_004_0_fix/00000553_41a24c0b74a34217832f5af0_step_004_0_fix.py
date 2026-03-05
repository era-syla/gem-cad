import cadquery as cq
import math

# Main dimensions
base_r = 50
base_h = 6
cone_bottom_r = 42
cone_top_r = 28
cone_h = 35
rim_r = 48
rim_h = 3

# Create the flat base disk
base = cq.Workplane("XY").circle(base_r).extrude(base_h)

# Create the truncated cone (frustum) on top of base
cone = (
    cq.Workplane("XY")
    .workplane(offset=base_h)
    .circle(cone_bottom_r)
    .workplane(offset=cone_h)
    .circle(cone_top_r)
    .loft()
)

result = base.union(cone)

# Add a slight rim/lip around the base edge
rim = (
    cq.Workplane("XY")
    .circle(base_r)
    .circle(base_r - 4)
    .extrude(rim_h + base_h)
)
# Actually skip separate rim - the base already forms it

# Add groove/channel near edge of base (circular groove on top face of base)
groove = (
    cq.Workplane("XY")
    .workplane(offset=base_h - 2)
    .circle(rim_r)
    .circle(rim_r - 3)
    .extrude(2)
)
result = result.cut(groove)

# Add small notches around base edge (4 notches)
for angle in [0, 90, 180, 270]:
    x = (base_r - 2) * math.cos(math.radians(angle))
    y = (base_r - 2) * math.sin(math.radians(angle))
    notch = (
        cq.Workplane("XY")
        .center(x, y)
        .box(8, 4, base_h + 1, centered=True)
    )
    result = result.cut(notch)

# Holes on top face of cone
top_z = base_h + cone_h

# Center hole
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(6, 8)
)

# Ring of holes on top face
hole_pattern_r = 15
n_ring_holes = 6
hole_dia = 5
hole_depth = 10

for i in range(n_ring_holes):
    angle = i * 360 / n_ring_holes
    x = hole_pattern_r * math.cos(math.radians(angle))
    y = hole_pattern_r * math.sin(math.radians(angle))
    cyl = (
        cq.Workplane("XY")
        .workplane(offset=top_z - hole_depth)
        .center(x, y)
        .circle(hole_dia / 2)
        .extrude(hole_depth + 1)
    )
    result = result.cut(cyl)

# Additional smaller holes in a tighter pattern
small_holes = [
    (7, 0), (-7, 0), (0, 7), (0, -7)
]
for (x, y) in small_holes:
    cyl = (
        cq.Workplane("XY")
        .workplane(offset=top_z - 6)
        .center(x, y)
        .circle(1.5)
        .extrude(7)
    )
    result = result.cut(cyl)

# Bottom face holes (mounting holes through base)
mount_hole_r = 40
n_mount = 4
for i in range(n_mount):
    angle = 45 + i * 90
    x = mount_hole_r * math.cos(math.radians(angle))
    y = mount_hole_r * math.sin(math.radians(angle))
    cyl = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(3)
        .extrude(base_h)
    )
    result = result.cut(cyl)