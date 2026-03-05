import cadquery as cq

# Parameters
body_len = 60
body_width = 8
body_height = 20
tab_w = 5
tab_h = 8
tab_depth = 10
sup_th = 2
sup_h = 12
sup_offset_x = body_len/2 - 5
arc_r = 20

# Main body
result = cq.Workplane("XY").box(body_len, body_width, body_height)

# Bottom tab
tab = (
    cq.Workplane("XY")
    .transformed(offset=(0, (body_width + tab_depth) / 2, -(body_height - tab_h) / 2))
    .box(tab_w, tab_depth, tab_h)
)
result = result.union(tab)

# Vertical supports for arch
sup1 = (
    cq.Workplane("XY")
    .transformed(offset=(sup_offset_x, 0, body_height/2 + sup_h/2))
    .box(sup_th, body_width, sup_h)
)
sup2 = (
    cq.Workplane("XY")
    .transformed(offset=(-sup_offset_x, 0, body_height/2 + sup_h/2))
    .box(sup_th, body_width, sup_h)
)
result = result.union(sup1).union(sup2)

# Arch path in XZ plane
path_wp = (
    cq.Workplane("XZ")
    .moveTo(-sup_offset_x, body_height + 1)
    .threePointArc((0, body_height + arc_r), (sup_offset_x, body_height + 1))
)
arc_wire = path_wp.val()

# Sweep a circular section along the arch path to form the handle
arch = (
    cq.Workplane("YZ")
    .workplane(offset=body_width/2)
    .circle(sup_th/2)
    .sweep(arc_wire)
)
result = result.union(arch)