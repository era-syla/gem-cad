import cadquery as cq

outer_shape = (
    cq.Workplane("XY")
    .polyline([(0, 0), (20, 0), (20, 80), (40, 80), (40, 100), (0, 100)])
    .close()
    .extrude(10)
)

inner_shape = (
    cq.Workplane("XY")
    .polyline([(5, 5), (15, 5), (15, 85), (35, 85), (35, 95), (5, 95)])
    .close()
    .extrude(10)
)

result = outer_shape.cut(inner_shape)