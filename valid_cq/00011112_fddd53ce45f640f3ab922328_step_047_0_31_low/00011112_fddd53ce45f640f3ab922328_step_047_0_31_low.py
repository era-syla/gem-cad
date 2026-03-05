import cadquery as cq

# Parameters
length = 40.0
width = 20.0
thickness = 10.0

cyl1_radius = 8.0
cyl1_height = 2.0

hole_radius = 3.0
csk_radius = 8.0
csk_angle = 90.0

pin_base_radius = 4.0
pin_base_length = 3.0
pin_radius = 2.5
pin_length = 10.0

# Base block
result = cq.Workplane("XY").box(length, width, thickness)

# Top features
# Left cylinder (raised)
result = (
    result.faces(">Z").workplane()
    .center(-length/4, 0)
    .circle(cyl1_radius)
    .extrude(cyl1_height)
)

# Right hole (countersunk)
result = (
    result.faces(">Z").workplane()
    .center(length/4, 0)
    .cskHole(hole_radius*2, csk_radius*2, csk_angle, depth=thickness)
)

# Side pin features
result = (
    result.faces(">X").workplane()
    .center(0, 0)
    .circle(pin_base_radius)
    .extrude(pin_base_length)
    .faces(">X").workplane()
    .center(0, 0)
    .circle(pin_radius)
    .extrude(pin_length)
)