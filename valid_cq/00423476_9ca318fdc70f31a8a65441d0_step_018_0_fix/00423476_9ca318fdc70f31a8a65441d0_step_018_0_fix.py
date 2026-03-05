import cadquery as cq

wall_thickness = 5
wall_height = 20
top_thickness = 5
bar_length = 100
depth = 10

dia_large = 10
dia_small = 4
margin_large = 8
margin_small = 4

inner = bar_length/2
left_inner = -inner
right_inner = inner
left_outer = left_inner - wall_thickness
right_outer = right_inner + wall_thickness

pts = [
    (left_outer, 0),
    (left_outer, wall_height),
    (left_inner, wall_height),
    (left_inner, wall_height - top_thickness),
    (right_inner, wall_height - top_thickness),
    (right_inner, wall_height),
    (right_outer, wall_height),
    (right_outer, 0),
]

result = cq.Workplane("XZ").polyline(pts).close().extrude(depth)

x_big_left = left_outer + margin_large
x_big_right = right_outer - margin_large
x_small_left = left_outer + margin_small
x_small_right = right_outer - margin_small

result = result.faces(">Z").workplane().pushPoints([(x_big_left, 0), (x_big_right, 0)]).hole(dia_large)
result = result.faces(">Z").workplane().pushPoints([(x_small_left, 0), (x_small_right, 0)]).hole(dia_small)