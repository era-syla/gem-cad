import cadquery as cq

# Parameters
base_l = 120
base_w = 60
base_t = 10
pocket_l = 80
pocket_w = 40
pocket_d = 7
wall_len = 60
wall_h = 40
wall_th = 10
hole_d = 5

# Base with pocket
result = (
    cq.Workplane("XY")
    .box(base_l, base_w, base_t)
    .faces(">Z")
    .workplane()
    .rect(pocket_l, pocket_w)
    .cutBlind(-pocket_d)
)

# Back wall
back_wall = (
    cq.Workplane(
        cq.Plane(origin=(-base_l/2 + wall_len/2, base_w/2, base_t/2), normal=(0, 1, 0))
    )
    .rect(wall_len, wall_h)
    .extrude(wall_th)
)
result = result.union(back_wall)

# Diagonal brace
brace = (
    cq.Workplane(
        cq.Plane(origin=(-base_l/2 + wall_len/2, base_w/2, base_t/2), normal=(0, 1, 0))
    )
    .polyline([(-wall_len/2, 0), (wall_len/2, wall_h), (wall_len/2, 0)])
    .close()
    .extrude(wall_th)
)
result = result.union(brace)

# Hole through brace (along X axis)
result = result.cut(
    cq.Workplane("XY")
    .transformed(
        offset=(
            0,
            base_w/2 + wall_th/2,
            base_t/2 + wall_h
        ),
        rotate=(0, 90, 0),
    )
    .circle(hole_d / 2)
    .extrude(base_l * 2)
)

# Hole in left side of base (along X axis)
result = (
    result.faces("<X")
    .workplane()
    .hole(hole_d, depth=base_l * 2)
)