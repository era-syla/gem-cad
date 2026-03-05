import cadquery as cq

# Parameters
length = 60.0
width = 30.0
height = 15.0

boss_dia = 24.0
boss_height = 2.5
boss_x = -15.0

hole_dia = 8.0
csk_dia = 22.0
csk_angle = 90.0
hole_x = 15.0

pin_base_dia = 13.0
pin_base_len = 3.5
pin_dia = 7.0
pin_len = 12.0

# Generate 3D model
result = (
    cq.Workplane("XY")
    .box(length, width, height)
    .faces(">Z")
    .tag("top_face")
    # Top cylindrical boss
    .workplaneFromTagged("top_face")
    .center(boss_x, 0)
    .circle(boss_dia / 2.0)
    .extrude(boss_height)
    # Top countersunk hole
    .workplaneFromTagged("top_face")
    .center(hole_x, 0)
    .cskHole(diameter=hole_dia, cskDiameter=csk_dia, cskAngle=csk_angle)
    # Side pin base
    .faces(">X")
    .workplane()
    .circle(pin_base_dia / 2.0)
    .extrude(pin_base_len)
    # Side pin shaft
    .faces(">X")
    .workplane()
    .circle(pin_dia / 2.0)
    .extrude(pin_len)
)