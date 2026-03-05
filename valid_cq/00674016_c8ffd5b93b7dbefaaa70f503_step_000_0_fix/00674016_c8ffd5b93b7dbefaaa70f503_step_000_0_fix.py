import cadquery as cq

# Parameters
cyl_OD, cyl_ID, cyl_H = 60, 50, 80
wall_thick, wall_width = 5, 80
plate_overhang, plate_thick = 20, 5
plate_y = cyl_OD + 20
x_min = -(cyl_OD/2 + wall_thick)
x_max = cyl_OD/2 + plate_overhang
plate_x = x_max - x_min
origin_x = (x_min + x_max) / 2
hole_dia, hole_margin = 5, 10
hole_rel = (x_max - hole_margin) - origin_x

result = (
    cq.Workplane("XY", origin=(origin_x, 0, 0))
      .rect(plate_x, plate_y)
      .extrude(plate_thick)
      .faces(">Z").workplane()
      .center(hole_rel, 0).hole(hole_dia)
      .faces(">Z").workplane()
      .center(-origin_x, 0)
      .circle(cyl_OD/2).circle(cyl_ID/2)
      .extrude(cyl_H)
      .faces(">Z").workplane()
      .center((x_min + wall_thick/2) - origin_x, 0)
      .rect(wall_thick, wall_width)
      .extrude(cyl_H)
)