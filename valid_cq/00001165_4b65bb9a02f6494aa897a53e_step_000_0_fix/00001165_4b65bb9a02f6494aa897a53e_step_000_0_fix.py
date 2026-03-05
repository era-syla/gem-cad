import cadquery as cq

# Parameters
cyl_r = 20
cyl_h = 30
tube_len = 60
tube_w = 25
tube_h = 50
thickness = 2
fillet_r = 5
angle = 30

# Base cylinder
cyl = cq.Workplane("XY").circle(cyl_r).extrude(cyl_h)

# Outer tube profile
tube_outer = (
    cq.Workplane("XY")
    .rect(tube_len, tube_w)
    .extrude(tube_h)
    .edges("|Z")
    .fillet(fillet_r)
)

# Inner cutout for hollow tube
tube_inner = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, thickness))
    .rect(tube_len - 2 * thickness, tube_w - 2 * thickness)
    .extrude(tube_h - thickness)
)

# Hollow tube
hollow_tube = tube_outer.cut(tube_inner)

# Position and rotate the tube so it intersects with the cylinder
tube = (
    hollow_tube
    .rotate((0, 0, 0), (1, 0, 0), -angle)
    .translate((cyl_r, 0, cyl_h))
)

# Combine cylinder and tube
result = cyl.union(tube)