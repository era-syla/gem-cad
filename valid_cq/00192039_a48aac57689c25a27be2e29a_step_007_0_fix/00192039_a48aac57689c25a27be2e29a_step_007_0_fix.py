import cadquery as cq

# Parameters
rod_r = 3
rod_len = 80

base_x = 30
base_y = 20
base_z = 5

cyl_r = rod_r + 1
slot_depth = 3
slot_height = cyl_r

# Build bracket
base = cq.Workplane("XY").box(base_x, base_y, base_z)

half_cyl = (
    cq.Workplane("XZ")
    .workplane(offset=base_z/2)
    .moveTo(-cyl_r, 0)
    .threePointArc((cyl_r, 0), (0, cyl_r))
    .lineTo(-cyl_r, 0)
    .close()
    .extrude(base_y)
)

bracket = base.union(half_cyl)

cut_box = (
    cq.Workplane("XY")
    .workplane(offset=base_z/2 + slot_height/2)
    .box(slot_depth, base_y + 2, slot_height + 2)
    .translate((cyl_r - slot_depth/2, 0, 0))
)

bracket = bracket.cut(cut_box).translate((0, 0, base_z/2))

# Build rod
rod = cq.Workplane("XY").circle(rod_r).extrude(rod_len)

# Combine
result = rod.union(bracket)