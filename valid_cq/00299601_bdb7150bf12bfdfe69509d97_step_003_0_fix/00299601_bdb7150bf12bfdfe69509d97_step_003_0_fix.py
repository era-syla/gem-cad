import cadquery as cq

outer_cylinder = cq.Workplane("XY").circle(10).extrude(40)
inner_cutout = cq.Workplane("XY").circle(5).extrude(40)

hole = cq.Workplane("XY").move(0, 20).circle(2).extrude(10)

side_square = cq.Workplane("XY").move(0, 20).box(8, 6, 6).edges("|Z").fillet(1)
side_hole = side_square.faces(">Y").workplane().hole(4)

result = (
    outer_cylinder
    .cut(inner_cutout)
    .cut(hole)
    .union(side_square)
    .cut(side_hole)
)