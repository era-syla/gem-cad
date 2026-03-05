import cadquery as cq

plate_l, plate_w, plate_t = 100, 60, 3
stud_d, stud_h = 5, 3
stud_offset_x, stud_offset_y = 40, 25
main_l, main_w, main_h = 80, 40, 20
sub_l, sub_w, sub_h = 30, 20, 10
cyl_od, cyl_id, cyl_h = 15, 10, 30

result = cq.Workplane("XY").box(plate_l, plate_w, plate_t)

dx = plate_l/2 - stud_offset_x
dy = plate_w/2 - stud_offset_y
stud_positions = [( dx,  dy), ( dx, -dy), (-dx,  dy), (-dx, -dy)]
result = result.faces(">Z").workplane().pushPoints(stud_positions).circle(stud_d/2).extrude(stud_h)

result = result.faces(">Z").workplane().rect(main_l, main_w).extrude(main_h)

offset_x = -(main_l/2 - sub_l/2)
result = result.faces(">Z").workplane().transformed(offset=(offset_x, 0, 0)).rect(sub_l, sub_w).extrude(sub_h)

result = result.faces(">Z").workplane(offset=sub_h).transformed(offset=(offset_x, 0, 0)).circle(cyl_od/2).extrude(cyl_h)

result = result.faces(">Z").workplane().cskHole(cyl_id, cyl_od, 90, depth=cyl_h)