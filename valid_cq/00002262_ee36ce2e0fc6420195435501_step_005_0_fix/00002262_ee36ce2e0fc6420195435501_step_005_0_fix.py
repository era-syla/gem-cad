import cadquery as cq

plate_dia = 100
plate_th = 5
boss1_dia = 40
boss1_h = 6
boss2_dia = 25
boss2_h = 3
hole_dia = 15

result = (
    cq.Workplane("XY")
    .circle(plate_dia/2).extrude(plate_th)
    .faces(">Z").workplane()
    .circle(boss1_dia/2).extrude(boss1_h)
    .faces(">Z").workplane()
    .circle(boss2_dia/2).extrude(boss2_h)
    .faces(">Z").workplane()
    .hole(hole_dia)
)