import cadquery as cq

# LEGO-like brick: 1x8 with studs on top, and a pin/axle on one end stud

# Standard LEGO dimensions (in mm)
stud_pitch = 8.0       # distance between stud centers
plate_height = 9.6     # standard brick height (3 plates)
wall_thickness = 1.5
stud_diameter = 4.8
stud_height = 1.8
stud_radius = stud_diameter / 2

num_studs = 8
brick_length = num_studs * stud_pitch  # 64mm
brick_width = stud_pitch               # 8mm (1 stud wide)
brick_height = plate_height            # 9.6mm

# Build base brick
result = (
    cq.Workplane("XY")
    .box(brick_length, brick_width, brick_height)
)

# Add studs on top - centered along X, centered along Y
# Box is centered at origin, so studs go from -brick_length/2 to +brick_length/2
stud_y = 0
stud_z = brick_height / 2 + stud_height / 2

for i in range(num_studs):
    stud_x = -brick_length / 2 + stud_pitch / 2 + i * stud_pitch
    result = (
        result
        .workplane(offset=brick_height / 2)
        .center(stud_x, stud_y)
        .circle(stud_radius)
        .extrude(stud_height)
    )

# Add axle/pin on top of the last stud (rightmost stud)
# The last stud center x
last_stud_x = -brick_length / 2 + stud_pitch / 2 + (num_studs - 1) * stud_pitch

# Pin dimensions
pin_radius = 1.5
pin_height = 12.0

result = (
    result
    .workplane(offset=brick_height / 2 + stud_height)
    .center(last_stud_x, stud_y)
    .circle(pin_radius)
    .extrude(pin_height)
)