import cadquery as cq

outer_R = 40
mid_R = 30
inner_R = 20
base_thickness = 4
groove_depth = 1
center_height = 2

base = cq.Workplane("XY").circle(outer_R).extrude(base_thickness)

groove_cutter = (
    cq.Workplane("XY")
    .circle(outer_R)
    .extrude(groove_depth)
    .cut(cq.Workplane("XY").circle(mid_R).extrude(groove_depth))
    .translate((0, 0, base_thickness - groove_depth))
)
base = base.cut(groove_cutter)

center = (
    cq.Workplane("XY", origin=(0, 0, base_thickness - groove_depth))
    .circle(inner_R)
    .extrude(center_height)
)
result = base.union(center)