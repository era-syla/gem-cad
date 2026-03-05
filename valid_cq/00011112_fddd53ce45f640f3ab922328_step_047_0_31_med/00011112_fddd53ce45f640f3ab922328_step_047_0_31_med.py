import cadquery as cq

# Parameters
length = 60.0
width = 30.0
height = 15.0

boss_radius = 12.0
boss_height = 3.0

hole_diam = 6.0
csk_diam = 22.0
csk_angle = 90.0

pin_base_radius = 6.5
pin_base_length = 4.0
pin_tip_radius = 3.5
pin_tip_length = 12.0

# Base block
base = cq.Workplane("XY").box(length, width, height)

# Top raised boss (left side)
result = (
    base.faces(">Z")
    .workplane()
    .center(-length / 4, 0)
    .circle(boss_radius)
    .extrude(boss_height)
)

# Top countersunk hole (right side)
result = (
    result.faces(">Z")
    .workplane()
    .center(length / 4, 0)
    .cskHole(diameter=hole_diam, cskDiameter=csk_diam, cskAngle=csk_angle)
)

# Side stepped pin (front/right face)
result = (
    result.faces(">X")
    .workplane()
    .circle(pin_base_radius)
    .extrude(pin_base_length)
    .faces(">X")
    .workplane()
    .circle(pin_tip_radius)
    .extrude(pin_tip_length)
)