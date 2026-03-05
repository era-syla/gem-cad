import cadquery as cq

plate_thickness = 10
center_hole_dia = 40
bolt_hole_dia = 10
bolt_hole_dist = 60
rim = 10

center_hole_radius = center_hole_dia / 2
bolt_hole_radius = bolt_hole_dia / 2
bolt_offset = bolt_hole_dist / 2

outer_center_radius = center_hole_radius + rim
outer_bolt_radius = bolt_hole_radius + rim

result = (
    cq.Workplane("XY")
    .circle(outer_center_radius)
    .pushPoints([(bolt_offset, 0), (-bolt_offset, 0)])
    .circle(outer_bolt_radius)
    .extrude(plate_thickness)
    .combine()
    .faces(">Z")
    .workplane()
    .circle(center_hole_radius)
    .pushPoints([(-bolt_offset, 0), (bolt_offset, 0)])
    .circle(bolt_hole_radius)
    .cutThruAll()
)