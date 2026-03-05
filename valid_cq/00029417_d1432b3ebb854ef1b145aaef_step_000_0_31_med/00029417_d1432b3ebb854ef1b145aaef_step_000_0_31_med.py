import cadquery as cq

# Parameters
bar_length = 150
bar_width = 16
thickness = 16

clamp_od = 34
clamp_id = 22

clamp_ext_length = 18
clamp_ext_width = 24
gap_width = 3
bolt_hole_dia = 6

# 1. Main cylinder
body = cq.Workplane("XY").cylinder(thickness, clamp_od / 2)

# 2. Main bar (extending to the right)
# Centered at bar_length/2, so it starts from X=0 and goes to X=bar_length
bar = cq.Workplane("XY").center(bar_length / 2, 0).box(bar_length, bar_width, thickness)
body = body.union(bar)

# 3. Front extension for the clamp (extending to the left)
# Overlap slightly with the cylinder to ensure a clean union
front_x_center = -clamp_od / 2 - clamp_ext_length / 2 + 2
front = cq.Workplane("XY").center(front_x_center, 0).box(clamp_ext_length + 4, clamp_ext_width, thickness)
body = body.union(front)

# 4. Main bore hole
body = body.faces(">Z").workplane().hole(clamp_id)

# 5. Split gap cut
# Box extending into the negative X direction to split the front extension
gap_cut = cq.Workplane("XY").center(-clamp_od, 0).box(clamp_od * 2, gap_width, thickness + 2)
body = body.cut(gap_cut)

# 6. Bolt hole across the front extension
# XZ workplane has its normal along the Y axis, so a cylinder here will cut across the gap
bolt_x = -clamp_od / 2 - clamp_ext_length / 2
bolt_hole_cut = cq.Workplane("XZ").center(bolt_x, 0).cylinder(clamp_ext_width + 10, bolt_hole_dia / 2)
body = body.cut(bolt_hole_cut)

# Final result
result = body