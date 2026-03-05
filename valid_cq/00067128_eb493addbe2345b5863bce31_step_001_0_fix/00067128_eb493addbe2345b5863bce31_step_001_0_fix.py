import cadquery as cq

size_main_body = (60, 20, 10)
diameter_holes = 15
diameter_inner_holes = 7
link_length = 10
link_size = (4, 2, 40)

main_body = cq.Workplane("XY").box(*size_main_body)

holes = (
    cq.Workplane("XY")
    .circle(diameter_holes / 2).extrude(size_main_body[2])
    .translate((-15, 0, 0))
    .union(
        cq.Workplane("XY")
        .circle(diameter_holes / 2)
        .extrude(size_main_body[2])
        .translate((15, 0, 0))
    )
)

inner_holes = (
    cq.Workplane("XY")
    .circle(diameter_inner_holes / 2).extrude(size_main_body[2])
    .translate((-15, 0, 0))
    .cut(
        cq.Workplane("XY")
        .circle(diameter_inner_holes / 2)
        .extrude(size_main_body[2])
        .translate((15, 0, 0))
    )
)

links = (
    cq.Workplane("XY")
    .rect(link_size[0], link_size[1])
    .extrude(size_main_body[2])
    .translate((0, size_main_body[1]/2 - link_length/2, 0))
    .union(
        cq.Workplane("XY")
        .rect(link_size[0], link_size[1])
        .extrude(size_main_body[2])
        .translate((0, -size_main_body[1]/2 + link_length/2, 0))
    )
)

result = main_body.cut(holes).cut(inner_holes).union(links)