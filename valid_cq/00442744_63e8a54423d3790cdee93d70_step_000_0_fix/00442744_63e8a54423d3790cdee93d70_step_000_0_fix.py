import cadquery as cq
import math

# Parameters
thickness = 3.0
fan_radius = 20.0
slot_count = 12
slot_width = 3.0
slot_depth = 8.0
body_width_top = 8.0
body_width_bottom = 15.0
body_height = 50.0
leg_length = 20.0
leg_width = 4.0
leg_gap = 8.0
center_slot_width = 12.0
center_slot_height = 8.0
foot_slot_width = 6.0
foot_slot_height = 3.0

# Derived Y positions
Y1 = -fan_radius
Y2 = Y1 - body_height
Y3 = Y2 - leg_length

# Create fan disk
fan = cq.Workplane("XY").circle(fan_radius).extrude(thickness)

# Create body & legs profile
body_profile = [
    ( body_width_top/2, Y1),
    ( body_width_bottom/2, Y2),
    ( leg_width/2,          Y2),
    ( leg_width/2,          Y3),
    (-leg_width/2,          Y3),
    (-body_width_bottom/2,  Y2),
    (-body_width_top/2,     Y1),
]
body = cq.Workplane("XY").polyline(body_profile).close().extrude(thickness)

# Fuse fan and body
result = fan.union(body)

# Cut radial slots in fan
for i in range(slot_count):
    angle = i * 360.0 / slot_count
    x = (fan_radius - slot_depth/2) * math.cos(math.radians(angle))
    y = (fan_radius - slot_depth/2) * math.sin(math.radians(angle))
    result = (
        result
        .faces(">Z")
        .workplane()
        .transformed(offset=(x, y, 0), rotate=(0, 0, angle))
        .rect(slot_width, slot_depth)
        .cutThruAll()
    )

# Cut center rectangular slot in body
center_slot_y = (Y1 + Y2) / 2
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, center_slot_y)
    .rect(center_slot_width, center_slot_height)
    .cutThruAll()
)

# Cut foot slots in legs
left_x = -(leg_gap/2 + leg_width/2)
right_x =  (leg_gap/2 + leg_width/2)
foot_y = Y3 + foot_slot_height/2
for x in (left_x, right_x):
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(x, foot_y)
        .rect(foot_slot_width, foot_slot_height)
        .cutThruAll()
    )