import cadquery as cq

# Parameters
inner_r = 14
th = 3
outer_r = inner_r + th
depth = 10
base_thk = 5
hinge_dia = 8
latch_th = 5
latch_h = 6

# Bottom‐half ring profile on XZ, extruded along Y
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_r, base_thk)
    .threePointArc((0, base_thk + outer_r), (-outer_r, base_thk))
    .lineTo(-inner_r, base_thk)
    .threePointArc((0, base_thk + inner_r), (inner_r, base_thk))
    .close()
)
ring = profile.extrude(depth)

# Base block
base_min_x = -outer_r
base_max_x = outer_r + hinge_dia
base_center_x = (base_min_x + base_max_x) / 2
base_width = base_max_x - base_min_x
base = (
    cq.Workplane("XZ")
    .center(base_center_x, 0)
    .box(base_width, depth, base_thk)
)

# Hinge pad (cylinder) on right side
hinge_center_x = outer_r + hinge_dia / 2
hinge = (
    cq.Workplane("XZ", origin=(hinge_center_x, 0, base_thk / 2))
    .circle(hinge_dia / 2)
    .extrude(depth)
)

# Latch block on left side
latch_center_x = -outer_r - latch_th / 2
latch = (
    cq.Workplane("XZ", origin=(latch_center_x, 0, base_thk + latch_h / 2))
    .box(latch_th, depth, latch_h)
)

result = ring.union(base).union(hinge).union(latch)