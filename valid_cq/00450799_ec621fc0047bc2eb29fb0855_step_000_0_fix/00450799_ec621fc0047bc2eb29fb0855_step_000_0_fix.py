import cadquery as cq

outer_radius = 10
inner_radius = 8
length = 40
outer_cylinder = cq.Workplane("XY").circle(outer_radius).extrude(length)
inner_cylinder = cq.Workplane("XY").circle(inner_radius).extrude(length)
cylinder = outer_cylinder.cut(inner_cylinder)

base_width = 24
base_height = 16
base_length = 20
base = (cq.Workplane("XY")
        .box(base_width, base_length, base_height)
        .translate((0, base_length / 2 + length / 2, base_height / 2)))

result = cylinder.union(base)