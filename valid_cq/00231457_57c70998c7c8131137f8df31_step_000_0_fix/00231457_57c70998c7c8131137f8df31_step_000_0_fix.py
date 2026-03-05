import cadquery as cq

# Parameters
tube_dia = 20
tube_len = 20
box_size = 30
cone_len = 15
pocket_w = 20
pocket_h = 15
pocket_d = box_size + 2  # ensure full cut into box

# Bottom cylinder
cyl_bottom = cq.Workplane("XY").circle(tube_dia/2).extrude(tube_len)

# Bottom frustum (circle to square)
frust_bottom = (
    cq.Workplane("XY")
    .workplane(offset=tube_len)
    .circle(tube_dia/2)
    .workplane(offset=cone_len)
    .rect(box_size, box_size)
    .loft()
)

# Middle square box
mid_box = (
    cq.Workplane("XY")
    .workplane(offset=tube_len + cone_len)
    .box(box_size, box_size, box_size, centered=(True, True, False))
)

# Top frustum (square to circle)
frust_top = (
    cq.Workplane("XY")
    .workplane(offset=tube_len + cone_len + box_size)
    .rect(box_size, box_size)
    .workplane(offset=cone_len)
    .circle(tube_dia/2)
    .loft()
)

# Top cylinder
cyl_top = (
    cq.Workplane("XY")
    .workplane(offset=tube_len + cone_len + box_size + cone_len)
    .circle(tube_dia/2)
    .extrude(tube_len)
)

# Combine all parts
result = cyl_bottom.union(frust_bottom).union(mid_box).union(frust_top).union(cyl_top)

# Pocket cut in the front of the box
pocket = (
    cq.Workplane("XZ", origin=(0, box_size/2, tube_len + cone_len + box_size/2))
    .rect(pocket_w, pocket_h)
    .extrude(-pocket_d)
)
result = result.cut(pocket)