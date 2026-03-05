import cadquery as cq

rod_eye_od = 10
rod_eye_id = 4
rod_eye_thickness = 5
rod_dia = 6
rod_length = 80
body_dia = 12
body_length = 60
body_eye_od = 14
body_eye_id = 5
body_eye_thickness = 6

result = (
    cq.Workplane("XY")
    .circle(rod_eye_od/2)
    .extrude(rod_eye_thickness)
    .faces(">Z")
    .workplane()
    .circle(rod_eye_id/2)
    .cutBlind(-rod_eye_thickness)
    .faces(">Z")
    .workplane()
    .circle(rod_dia/2)
    .extrude(rod_length)
    .faces(">Z")
    .workplane()
    .circle(body_dia/2)
    .extrude(body_length)
    .faces(">Z")
    .workplane()
    .circle(body_eye_od/2)
    .extrude(body_eye_thickness)
    .faces(">Z")
    .workplane()
    .circle(body_eye_id/2)
    .cutBlind(-body_eye_thickness)
)