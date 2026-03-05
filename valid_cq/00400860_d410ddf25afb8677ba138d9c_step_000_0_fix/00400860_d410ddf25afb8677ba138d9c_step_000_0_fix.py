import cadquery as cq

# Parameters
length = 100
width = 10
thickness = 5
outer_hole_dia = 3
csk_dia = 6
csk_angle = 90
center_hole_dia = 3
end_margin = 8
offset = length/2 - end_margin

result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z").workplane()
    .pushPoints([(-offset, 0), (offset, 0)])
    .cskHole(outer_hole_dia, csk_dia, csk_angle)
    .pushPoints([(0, 0)])
    .hole(center_hole_dia)
)